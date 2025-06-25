__________________________________________________________________________

como prerequisito instale:
python https://www.python.org/downloads/   
procure una version superior a 3.12.0 y ejecutelo para instalarlo
nvm desde https://github.com/coreybutler/nvm-windows/releases  
el archivo setup.exe y ejecutelo para instalarlo
__________________________________________________________________________

en la carpeta de este git descargue solo el archivo
start_1.bat y ejecuteloa continuacion ese archivo creara la carpeta
de destino contabilidad.django y descargara el repositorio 
__________________________________________________________________________

abra la carpeta y busque el archivo 
start_2.bat y ejecutelo ese archivo instalara los paquetes y herramientas
nesesarias para que el software inicie de modo satisfactorio
__________________________________________________________________________

para inicar el software desepues de los pasos anteriores ubique el archivo
start_3.bat y ejecutelo, este creara dos ventanas de cmd y correra los 
servidores de backend django y frontend react.
__________________________________________________________________________

estructura encarpetado

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





