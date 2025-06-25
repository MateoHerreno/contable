@echo off
echo ================================
echo  Iniciando backend Django...
echo ================================
start cmd /k "cd start && ..\venv\Scripts\activate && python ../manage.py runserver"

echo ================================
echo  Iniciando frontend React...
echo ================================
start cmd /k "cd frontend_modfinanciero && npm start"
