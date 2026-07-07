@echo off
cd /d "C:\Users\Jean Jacques\Documents\velocoach-ai"

REM --- Démarre le serveur Python en arrière-plan ---
start "VeloCoach Server" /min python server.py

REM --- Laisse 2s au serveur pour démarrer ---
timeout /t 2 /nobreak >nul

REM --- Ouvre l'app en HTTP avec cache-bust (?v=timestamp) ---
start "" "http://localhost:8765/index.html?v=%RANDOM%"

exit