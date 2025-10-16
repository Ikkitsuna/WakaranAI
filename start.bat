@echo off
REM Script de lancement rapide pour Game Translator
REM Lance en mode administrateur pour les permissions hotkey

echo ============================================
echo  Game Translator - Lancement
echo ============================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH
    echo.
    echo Installez Python depuis: https://www.python.org/downloads/
    echo N'oubliez pas de cocher "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

REM Vérifier si Ollama tourne
echo [INFO] Verification d'Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo [AVERTISSEMENT] Ollama ne semble pas accessible
    echo Assurez-vous qu'Ollama est lance
    echo.
)

REM Lancer l'application
echo [INFO] Lancement de Game Translator...
echo.
python main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERREUR] L'application s'est arretee avec une erreur
    pause
)
