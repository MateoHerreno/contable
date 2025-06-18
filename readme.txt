 
instalar enviroment
python -m venv env
clonar
https://github.com/MateoHerreno/contable.git


encender entornor virtual
windows: env\Scripts\activate
linux: source env/bin/activate

pip install -r requirements.txt

para arrancar el servidor navegar sotware_contable\contabilidad
ejecutar 
python manage.py runserver   

comits
añadido

estructura actual
software_contable
├──contabilidad/
|   ├── contabilidad/            # Config principal de Django
|   │   ├── asgi.py
|   │   ├── settings.py
|   │   ├── urls.py              #url globales
|   │   └── wsgi.py
|   ├── modulo_financiero/       # Tu API completa
|   │   ├── >_pycache_
|   │   ├── > migrations          #todos los makemigrations antes de irese a la db
|   │   ├── _initi_
|   │   ├── admin.py             #todo lo que se imprime en djangoadmin
|   │   ├── apps.py               
|   │   ├── authentication.py    #sobreescritura de clases de django creacion usuario y super user para djangoadmin
|   │   ├── models.py            #modelos de base de datos
|   │   ├── permissions.py       #permisos y restricciones por rol
|   │   ├── serializers.py       #contruccion de la api desde restframe
|   │   ├── signals.py           #señalizacion de perfiles para arranque
|   │   ├── test.py
|   │   ├── urls.py              #todos los endpoints creados para la api de modulo_financiero
|   │   ├── utils.py             #utlidades varias como generacion de tokens, humanizar numeros grandes, export de pdf
|   │   ├── views.py             #toda la logica se integra para hacer una url y usarla en urls
|   │   ├── zpermisos_defin...   #todos los permisos personalizados definidos que se cargan por defecto
|   │   └── zpermisos.txt        #todos los permisos personalizados para usar en django shell
|   ├── frontend/                # Carpeta nueva para el proyecto React    |
|   │   ├── public/                                                        |
|   │   ├── src/                                                           | pendiente
|   │   ├── package.json                                                   |
|   │   └── build/               # Aquí se genera el build al compilar
|   ├── statics/                 # statics swagger
|   ├── staticfiles/             # Para collectstatic
|   ├── .env                     #variables de entorno a asegurar
|   ├── db.sqlite3               #base de datos
|   ├── mange.py                                
|   └── requirements.txt         #requerimientos para correr el proyecto
├── >docs                        # documentos de logica de negocio y fotos de jsons para algunos endpoints
├── >env                         # virtual enviroment (burbuja de desarrollo)
├──.gitignore                    #cosas para ignorar en git
└── README.txt                   #<----------------------------------ESTAS AQUI
