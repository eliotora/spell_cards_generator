@echo off
setlocal enabledelayedexpansion

:: Vérifie qu'un numéro de version est passé en paramètre
if "%~1"=="" (
    echo Usage: build.bat VERSION
    echo Exemple: build.bat 1.2.3
    exit /b 1
)

set VERSION=%~1
set ROOT=%~dp0
set DIST=%ROOT%dist
set INTERNAL=%DIST%\_internal
set INNO="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
set ISS="C:\Users\eliot_cosyn\Documents\TempProjects\spell_cards_generator\spell_cards_generator\setup.iss"

echo ======================================
echo   Build de la version %VERSION%
echo ======================================

:: 1. Mettre à jour version.json
echo {"version": "%VERSION%", "url": "https://github.com/eliotora/spell_cards_generator/releases/latest/download/SpellViewerInstaller.exe"} > "%ROOT%version.json"
echo [OK] version.json mis à jour
pause

:: 2. Construire avec PyInstaller
pyinstaller main.spec --noconfirm
if errorlevel 1 (
    echo [ERREUR] PyInstaller a échoué
    exit /b 1
)
echo [OK] PyInstaller terminé
pause

:: 3. Réorganiser les dossiers
if exist "%DIST%\images" rmdir /s /q "%DIST%\images"
if exist "%DIST%\styles" rmdir /s /q "%DIST%\styles"
if exist "%DIST%\export" rmdir /s /q "%DIST%\export"
if exist "%INTERNAL%\data" rmdir /s /q "%INTERNAL%\data"
if exist "%INTERNAL%\output" rmdir /s /q "%INTERNAL%\output"

move "%INTERNAL%\images" "%DIST%\images"
move "%INTERNAL%\styles" "%DIST%\styles"
move "%INTERNAL%\export" "%DIST%\export"

:: 4. Replacer version.json au bon endroit
if exist "%INTERNAL%\version.json" (
    move "%INTERNAL%\version.json" "%DIST%\version.json"
)

:: 5. Copier l'icône
copy /Y "%ROOT%app.ico" "%DIST%\app.ico"

pause

:: 6. Compiler le setup avec Inno Setup
%INNO% /DAppVersion=%VERSION% %ISS%
if errorlevel 1 (
    echo [ERREUR] Compilation Inno Setup a échoué
    exit /b 1
)

echo ======================================
echo   Build %VERSION% terminé avec succès !
echo ======================================

endlocal
