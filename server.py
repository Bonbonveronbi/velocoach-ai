"""
VeloCoach AI - serveur local ICU
Lance avec : "E:\\python\\python.exe" server.py
Repond sur http://localhost:8765
"""
import http.server, urllib.request, urllib.error, json, base64, threading, os
from datetime import date, timedelta

API_KEY    = "38iemxjyvrau0u5qbao3nkrlg"
ATHLETE_ID = "45440995"
PORT       = 8765
BASE       = f"https://intervals.icu/api/v1/athlete/{ATHLETE_ID}"
AUTH       = base64.b64encode(f"API_KEY:{API_KEY}".encode()).decode()
HEADERS    = {
    "Authorization": f"Basic {AUTH}",
    "Accept": "application/json",
    "User-Agent": "VeloCoachAI/1.0"
}

# Dossier contenant index.html (même dossier que server.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def icu_get(path):
    req = urllib.request.Request(BASE + path, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def icu_post(path, payload):
    body = json.dumps(payload).encode()
    req  = urllib.request.Request(
        BASE + path, data=body,
        headers={**HEADERS, "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        # Sert index.html sur / ou /index.html
        if self.path.split('?')[0] in ('/', '/index.html'):
            html_path = os.path.join(BASE_DIR, 'index.html')
            try:
                with open(html_path, 'rb') as f:
                    body = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                self.end_headers()
                self.wfile.write(body)
            except FileNotFoundError:
                self._error(404, 'index.html introuvable')
            return

        # GET /all ou /wellness+activites
        if self.path.split('?')[0] in ('/all', '/data'):
            today = date.today().isoformat()
            d20   = (date.today() - timedelta(days=20)).isoformat()
            d45   = (date.today() - timedelta(days=45)).isoformat()

            results = {}
            errors  = {}

            def fetch_wellness():
                try:
                    results["wellness"] = icu_get(f"/wellness?oldest={d20}&newest={today}")
                except Exception as e:
                    errors["wellness"] = str(e)

            def fetch_activities():
                try:
                    acts = icu_get(f"/activities?oldest={d45}&newest={today}&limit=20")
                    acts.sort(key=lambda a: a.get("start_date_local", ""), reverse=True)
                    results["activities"] = acts
                except Exception as e:
                    errors["activities"] = str(e)

            t1 = threading.Thread(target=fetch_wellness)
            t2 = threading.Thread(target=fetch_activities)
            t1.start(); t2.start()
            t1.join(); t2.join()

            self._json({
                "wellness":   results.get("wellness", []),
                "activities": results.get("activities", []),
                "generated":  today,
                **({"errors": errors} if errors else {})
            })
            return

        self._error(404, "Not found")

    def do_POST(self):
        if self.path != "/workout":
            self._error(404, "Not found"); return
        try:
            length  = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length))
            event = {
                "category":         "WORKOUT",
                "start_date_local": payload["date"] + "T09:00:00",
                "name":             payload.get("name", "Seance VeloCoach"),
                "description":      payload.get("description", ""),
                "type":             payload.get("type", "Ride"),
                "indoor":           payload.get("indoor", False),
            }
            if payload.get("load"):
                event["load"] = payload["load"]
            result = icu_post("/events", event)
            self._json({"ok": True, "event_id": result.get("id"), "event": result})
        except urllib.error.HTTPError as e:
            self._error(e.code, f"ICU {e.code}: {e.read().decode()}")
        except Exception as e:
            self._error(502, str(e))

    def _json(self, data):
        try:
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self._cors()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            self.wfile.flush()
        except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError):
            pass

    def _error(self, code, msg):
        try:
            body = json.dumps({"error": msg}).encode("utf-8")
            self.send_response(code)
            self._cors()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            self.wfile.flush()
        except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError):
            pass

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

if __name__ == "__main__":
    server = http.server.HTTPServer(("localhost", PORT), Handler)
    print(f"VeloCoach ICU server -> http://localhost:{PORT}")
    print(f"  Ouvre http://localhost:{PORT} dans ton navigateur")
    print(f"  GET  /all      -> wellness + activites ICU")
    print(f"  POST /workout  -> cree une seance sur ICU")
    print("Ctrl+C pour arreter")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nArret.")
