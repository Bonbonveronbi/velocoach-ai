@echo off
cd /d "C:\Users\Jean Jacques\Documents\velocoach-ai"

echo === Verification de Python ===
where python >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] "python" introuvable dans le PATH.
    echo Essaie de taper : where py
    echo Si "py" fonctionne mais pas "python", dis-le moi.
    pause
    exit /b 1
)
echo OK, python trouve.
echo.

echo === Ouverture du navigateur dans 2s ===
start "" "http://localhost:8765/index.html?v=%RANDOM%"
timeout /t 2 /nobreak >nul

echo === Demarrage du serveur ===
echo (Cette fenetre reste ouverte tant que le serveur tourne. Ctrl+C pour arreter.)
echo.
python server.py

echo.
echo === Le serveur s'est arrete ou a plante (voir message ci-dessus) ===
pause
