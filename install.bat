@echo off
title Game Translator - Installation
color 0B
echo.
echo ========================================
echo    GAME TRANSLATOR - INSTALLATION
echo ========================================
echo.

REM V\u00e9rifier Python
echo [1/4] Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH !
    echo.
    echo Veuillez installer Python 3.11 ou 3.12 depuis :
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Cochez "Add Python to PATH" lors de l'installation !
    pause
    exit /b 1
)

python --version
echo [OK] Python detecte !
echo.

REM V\u00e9rifier si venv311 existe d\u00e9j\u00e0
if exist "venv311" (
    echo [2/4] Environnement virtuel venv311 deja present
    choice /C YN /M "Voulez-vous le recreer (Y) ou le conserver (N)"
    if errorlevel 2 goto skip_venv
    if errorlevel 1 (
        echo Suppression de l'ancien venv311...
        rmdir /s /q venv311
    )
)

REM Cr\u00e9er l'environnement virtuel
echo [2/4] Creation de l'environnement virtuel venv311...
python -m venv venv311
if errorlevel 1 (
    color 0C
    echo [ERREUR] Impossible de creer l'environnement virtuel !
    echo Verifiez que le module venv est installe.
    pause
    exit /b 1
)
echo [OK] Environnement virtuel cree !
echo.

:skip_venv

REM Mise \u00e0 jour de pip
echo [3/4] Mise a jour de pip...
venv311\Scripts\python.exe -m pip install --upgrade pip
echo [OK] pip mis a jour !
echo.

REM Installation des d\u00e9pendances
echo [4/4] Installation des dependances...
echo Cela peut prendre quelques minutes...
echo.
venv311\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    color 0C
    echo [ERREUR] L'installation des dependances a echoue !
    echo Verifiez le fichier requirements.txt et votre connexion internet.
    pause
    exit /b 1
)

echo.
echo ========================================
echo    INSTALLATION TERMINEE AVEC SUCCES !
echo ========================================
echo.
echo Prochaines etapes :
echo   1. Lancez Ollama : ollama serve
echo   2. Double-cliquez sur RUN.bat pour demarrer
echo   3. Ou sur CONFIGURE.bat pour configurer
echo.
echo Si vous voulez utiliser EasyOCR (Python 3.11/3.12 uniquement) :
echo   - Decommenter les lignes dans requirements.txt
echo   - Relancer install.bat
echo.
pause
