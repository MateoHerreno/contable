@echo off
setlocal

REM =============================
REM CONFIGURACIÓN DEL REPO Y VERSIONES
set "REPO_URL=https://github.com/MateoHerreno/contable.git"
set "PROJECT_FOLDER=contabilidad_django"
set "NODE_VERSION=18.16.0"
REM =============================

echo ================================
echo 🔄 Verificando si ya existe la carpeta %PROJECT_FOLDER%...
if not exist "%PROJECT_FOLDER%" (
    echo 📥 Clonando el repositorio desde:
    echo     %REPO_URL%
    git clone %REPO_URL% %PROJECT_FOLDER%
) else (
    echo ✅ Carpeta ya existe: %PROJECT_FOLDER%
)

cd %PROJECT_FOLDER%

REM ================================
echo 🔍 Verificando Python...
where python >nul 2>nul
if errorlevel 1 (
    echo ❌ Python no está instalado. Descárgalo desde https://www.python.org/downloads/
    pause
    exit /b
)

REM ================================
echo 🔍 Verificando NVM...
where nvm >nul 2>nul
if errorlevel 1 (
    echo ❌ NVM no está instalado. Descárgalo desde https://github.com/coreybutler/nvm-windows
    pause
    exit /b
)

REM ================================
echo 🔁 Activando Node.js %NODE_VERSION%...
nvm use %NODE_VERSION%
if errorlevel 1 (
    echo ❌ No se pudo activar Node.js %NODE_VERSION%.
    echo 👉 Ejecuta: nvm install %NODE_VERSION%
    pause
    exit /b
)

