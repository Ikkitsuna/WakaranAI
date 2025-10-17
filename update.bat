@echo off
title Game Translator - Mise a jour
color 0B
echo.
echo ========================================
echo    GAME TRANSLATOR - MISE A JOUR
echo ========================================
echo.

REM V\u00e9rifier que l'installation existe
if not exist "venv311\Scripts\python.exe" (
    color 0C
    echo [ERREUR] Installation non detectee !
    echo Veuillez d'abord lancer INSTALL.bat
    pause
    exit /b 1
)

REM V\u00e9rifier si Git est install\u00e9
git --version >nul 2>&1
if errorlevel 1 (
    color 0E
    echo ========================================
    echo   Git non detecte - Mise a jour manuelle
    echo ========================================
    echo.
    echo Git n'est pas installe. Deux options :
    echo.
    echo 1. Installer Git depuis https://git-scm.com/
    echo 2. Telecharger manuellement depuis GitHub
    echo.
    echo Pour une mise a jour manuelle des dependances uniquement :
    choice /C YN /M "Mettre a jour uniquement les dependances Python"
    if errorlevel 2 exit /b 0
    goto update_deps
)

REM V\u00e9rifier si c'est un d\u00e9p\u00f4t Git
if not exist ".git" (
    color 0E
    echo ========================================
    echo   Depot Git non initialise
    echo ========================================
    echo.
    echo Ce dossier n'est pas un depot Git.
    echo.
    echo Pour activer les mises a jour automatiques :
    echo   1. Clonez le projet depuis GitHub
    echo   2. Ou initialisez Git : git init
    echo.
    echo Pour le moment, mise a jour des dependances uniquement :
    goto update_deps
)

REM Sauvegarder la configuration
echo [1/3] Sauvegarde de la configuration...
if exist "config.json" (
    copy /Y config.json config.json.backup >nul
    echo [OK] Configuration sauvegardee !
)
echo.

REM Tirer les derni\u00e8res modifications
echo [2/3] Telechargement des mises a jour depuis GitHub...
git pull
if errorlevel 1 (
    color 0C
    echo [ERREUR] Echec du telechargement !
    echo Verifiez votre connexion et les conflits Git.
    pause
    exit /b 1
)
echo [OK] Code mis a jour !
echo.

:update_deps
REM Mettre \u00e0 jour les d\u00e9pendances
echo [3/3] Mise a jour des dependances Python...
venv311\Scripts\python.exe -m pip install --upgrade pip
venv311\Scripts\python.exe -m pip install -r requirements.txt --upgrade
if errorlevel 1 (
    color 0C
    echo [ERREUR] Echec de la mise a jour des dependances !
    pause
    exit /b 1
)
echo [OK] Dependances mises a jour !
echo.

REM Restaurer la configuration si n\u00e9cessaire
if exist "config.json.backup" (
    echo Voulez-vous restaurer votre ancienne configuration ?
    choice /C YN /M "Restaurer config.json"
    if errorlevel 1 if not errorlevel 2 (
        copy /Y config.json.backup config.json >nul
        echo [OK] Configuration restauree !
    )
    del config.json.backup
)

echo.
echo ========================================
echo   MISE A JOUR TERMINEE AVEC SUCCES !
echo ========================================
echo.
echo Vous pouvez maintenant lancer RUN.bat
echo.
pause
