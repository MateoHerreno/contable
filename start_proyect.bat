echo -------------------------------
echo Creando entorno virtual...
echo -------------------------------
python -m venv venv

echo -------------------------------
echo Activando entorno virtual...
echo -------------------------------
call venv\Scripts\activate

echo -------------------------------
echo Instalando dependencias...
echo -------------------------------
pip install --upgrade pip
pip install -r requirements.txt

echo -------------------------------
echo Backend listo.
echo -------------------------------