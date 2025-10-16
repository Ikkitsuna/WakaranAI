@echo off
REM Script de test de l'installation

echo ============================================
echo  Game Translator - Test d'installation
echo ============================================
echo.

REM Vérifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python non installe
    exit /b 1
)

REM Lancer le script de test
python test_setup.py

pause
