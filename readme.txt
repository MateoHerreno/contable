 
instalar enviroment
python -m venv venv
clonar
https://github.com/MateoHerreno/contable.git


encender entornor virtual
windows: venv\Scripts\activate
linux: source env/bin/activate


para arrancar el servidor navegar sotware_contable\contabilidad
ejecutar 
pip install -r requirements.txt
python manage.py runserver   

estructura actual

contabilidad_django/
  |
  ├── backend_modfinanciero/       # Tu API completa
  │   ├── > _pycache_
  │   ├── > migrations         #todos los makemigrations antes de irese a la db
  │   ├── _initi_
  │   ├── admin.py             #todo lo que se imprime en djangoadmin
  │   ├── apps.py               
  │   ├── authentication.py    #sobreescritura de clases de django creacion usuario y super user para djangoadmin
  │   ├── models.py            #modelos de base de datos
  │   ├── permissions.py       #permisos y restricciones por rol
  │   ├── serializers.py       #contruccion de la api desde restframe
  │   ├── signals.py           #señalizacion de perfiles para arranque
  │   ├── test.py
  │   ├── urls.py              #todos los endpoints creados para la api de modulo_financiero
  │   ├── utils.py             #utlidades varias como generacion de tokens, humanizar numeros grandes, export de pdf
  │   ├── views.py             #toda la logica se integra para hacer una url y usarla en urls
  │   └── zpermisos_defin...   #todos los permisos personalizados definidos que se cargan por defecto  
  |
  ├── frontend__modfinanciero/ 
  │   ├── > node_modules
  │   ├── > src        
  │   ├── .gitignore           #cosas para ignorar en git
  │   ├── package-lockson.json          
  │   ├── package.json              
  │   └──  README.md    
  |
  ├── start/                   # Config principal de Django
  │   ├── asgi.py
  │   ├── settings.py
  │   ├── urls.py              #url globales
  │   └── wsgi.py
  |
  ├── > statics                # statics swagger
  ├── > staticfiles            # Para collectstatic
  ├── > venv                   # virtual enviroment (burbuja de desarrollo)
  ├── > zdocs                  # documentos de logica de negocio y fotos de jsons para algunos endpoints
  ├── .env                     #variables de entorno a asegurar
  ├──.gitignore                #cosas para ignorar en git
  ├── db.sqlite3               #base de datos
  ├── endpints_json.txt        # documentacion de endpoints de back
  ├── mange.py                 # archivo base de django para iniciar
  ├── README.txt               #<----------------------------------ESTAS AQUI         
  └── requirements.txt         #requerimientos para correr el proyecto





