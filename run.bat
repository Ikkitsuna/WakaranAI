@echo off
title Game Translator - Lanceur
color 0B

REM V\u00e9rifier que l'installation a \u00e9t\u00e9 faite
if not exist "venv311\Scripts\python.exe" (
    color 0C
    echo ========================================
    echo   ERREUR: Installation non detectee !
    echo ========================================
    echo.
    echo Veuillez d'abord lancer INSTALL.bat
    echo.
    pause
    exit /b 1
)

REM V\u00e9rifier qu'Ollama est accessible
echo Verification d'Ollama...
curl -s http://localhost:11434/api/version >nul 2>&1
if errorlevel 1 (
    color 0E
    echo ========================================
    echo   AVERTISSEMENT: Ollama non detecte
    echo ========================================
    echo.
    echo Ollama ne semble pas lance.
    echo Veuillez demarrer Ollama avant d'utiliser Game Translator :
    echo   ^> ollama serve
    echo.
    echo Ou verifiez qu'Ollama est installe :
    echo   https://ollama.ai/
    echo.
    choice /C YN /M "Continuer quand meme"
    if errorlevel 2 exit /b 1
)

cls
echo ========================================
echo      GAME TRANSLATOR - DEMARRAGE
echo ========================================
echo.
echo Lancement de Game Translator...
echo.
echo Instructions :
echo   - Ctrl+Shift+T : Traduire une zone
echo   - Ctrl+Shift+M : Changer de mode
echo   - Ctrl+C : Quitter
echo.
echo ========================================
echo.

REM Lancer l'application
venv311\Scripts\python.exe main.py

REM Si l'application s'arr\u00eate avec une erreur
if errorlevel 1 (
    color 0C
    echo.
    echo ========================================
    echo   ERREUR lors de l'execution
    echo ========================================
    echo.
    echo Verifiez les messages ci-dessus pour plus d'informations.
    echo.
)

pause
