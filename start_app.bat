@echo off
echo ================================
echo  Activando entorno virtual...
echo ================================
call venv\Scripts\activate

echo ================================
echo  Iniciando backend Django...
echo ================================
start cmd /k "cd start && python ../manage.py runserver"

echo ================================
echo  Iniciando frontend React...
echo ================================
start cmd /k "cd frontend_modfinanciero && npm start"