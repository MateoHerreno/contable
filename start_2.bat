REM ----- BACKEND -----
echo.
echo ================================
echo [1/3] Creando entorno virtual...
python -m venv venv

echo Activando entorno virtual...
call venv\Scripts\activate

echo [2/3] Instalando dependencias del backend...
pip install --upgrade pip
pip install -r requirements.txt

REM ----- FRONTEND -----
echo.
echo ================================
echo [3/3] Instalando dependencias del frontend...
cd frontend_modfinanciero
call npm install
cd ..

echo ================================
echo ✅ Proyecto configurado exitosamente con:
echo    - Node.js %NODE_VERSION%
echo    - Python
echo ================================
pause
