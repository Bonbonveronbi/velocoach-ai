#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VeloCoach AI — serveur local
- Sert les fichiers statiques (index.html) sur http://localhost:8765/
- GET  /all      -> wellness (42 j) + activities (45 j) depuis Intervals.icu
- POST /workout  -> crée une séance structurée dans le calendrier ICU
Aucune dépendance externe : Python 3 standard uniquement.

Lancer :  python server.py
"""

import sys
# FIX Windows : la console cp1252 par défaut plante sur les caractères
# unicode (→, ⚠, etc.) utilisés dans les print() ci-dessous. On force
# stdout/stderr en UTF-8 (Python 3.7+).
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import base64
import datetime
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from http.server import SimpleHTTPRequestHandler

# ════════════════════════════════════════════════════════════════════
#  CONFIG  —  À RENSEIGNER
# ════════════════════════════════════════════════════════════════════
ICU_ATHLETE_ID = "45440995"                 # sans le préfixe "i"
ICU_API_KEY    = "6k0yg9vyahohhoowgzih2u87y"     # Settings > Developer > API Key
PORT           = 8765
WELLNESS_DAYS  = 42
ACT_DAYS       = 45
# ════════════════════════════════════════════════════════════════════

ICU_BASE = "https://intervals.icu/api/v1"


def _auth_header():
    # ICU : Basic auth, username littéral "API_KEY", password = la clé
    raw = f"API_KEY:{ICU_API_KEY}".encode("utf-8")
    return "Basic " + base64.b64encode(raw).decode("ascii")


def _icu_get(path):
    req = urllib.request.Request(ICU_BASE + path, method="GET")
    req.add_header("Authorization", _auth_header())
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) VeloCoach/1.0")
    req.add_header("Accept", "application/json")
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def _icu_post(path, body):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(ICU_BASE + path, data=data, method="POST")
    req.add_header("Authorization", _auth_header())
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) VeloCoach/1.0")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch_all():
    today = datetime.date.today()
    w_old = (today - datetime.timedelta(days=WELLNESS_DAYS)).isoformat()
    a_old = (today - datetime.timedelta(days=ACT_DAYS)).isoformat()
    newest = today.isoformat()

    out = {"wellness": [], "activities": [],
           "generated": newest, "errors": {}}

    # Les 2 appels ICU sont indépendants -> on les lance en parallèle
    # pour rester bien sous le timeout de 15s côté navigateur.
    with ThreadPoolExecutor(max_workers=2) as ex:
        fut_w = ex.submit(_icu_get,
            f"/athlete/{ICU_ATHLETE_ID}/wellness?oldest={w_old}&newest={newest}")
        fut_a = ex.submit(_icu_get,
            f"/athlete/{ICU_ATHLETE_ID}/activities?oldest={a_old}&newest={newest}")

        try:
            out["wellness"] = fut_w.result()
        except urllib.error.HTTPError as e:
            out["errors"]["wellness"] = f"HTTP Error {e.code}: {e.reason}"
        except Exception as e:
            out["errors"]["wellness"] = str(e)

        try:
            out["activities"] = fut_a.result()
        except urllib.error.HTTPError as e:
            out["errors"]["activities"] = f"HTTP Error {e.code}: {e.reason}"
        except Exception as e:
            out["errors"]["activities"] = str(e)

    return out


def create_workout(w):
    """w = {name, date, type, load, description}"""
    date = w.get("date") or datetime.date.today().isoformat()
    body = {
        "category":          "WORKOUT",
        "start_date_local":  f"{date}T00:00:00",
        "type":              w.get("type", "Ride"),
        "name":              w.get("name", "Séance VeloCoach"),
        "description":       w.get("description", ""),
    }
    if w.get("load"):
        body["icu_training_load"] = int(w["load"])
    created = _icu_post(f"/athlete/{ICU_ATHLETE_ID}/events", body)
    return {"ok": True, "id": created.get("id"), "event": created}


class Handler(SimpleHTTPRequestHandler):

    def _send_json(self, obj, code=200):
        payload = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path.split("?")[0] == "/all":
            try:
                self._send_json(fetch_all())
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
            return
        # sinon : fichiers statiques (index.html, etc.)
        super().do_GET()

    def do_POST(self):
        if self.path.split("?")[0] == "/workout":
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = json.loads(self.rfile.read(length).decode("utf-8"))
                self._send_json(create_workout(body))
            except urllib.error.HTTPError as e:
                self._send_json({"ok": False,
                                 "error": f"ICU {e.code}: {e.reason}"}, 200)
            except Exception as e:
                self._send_json({"ok": False, "error": str(e)}, 200)
            return
        self.send_error(404)

    def log_message(self, fmt, *args):
        print("·", fmt % args)


if __name__ == "__main__":
    if ICU_API_KEY == "COLLE_TA_CLE_API_ICI":
        print("[!] Renseigne ICU_API_KEY en haut du fichier (Settings > Developer).")
    print(f"VeloCoach server -> http://localhost:{PORT}/index.html")
    print(f"  test API       -> http://localhost:{PORT}/all")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
