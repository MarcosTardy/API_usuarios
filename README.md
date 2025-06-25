##Descripción

Este proyecto es una API RESTful para gestionar usuarios, creada con FastAPI. Permite realizar operaciones CRUD (crear, leer, actualizar, eliminar) sobre usuarios, implementando seguridad mediante JWT/OAuth para autenticación y autorización. Los datos se almacenan en una base de datos remota en MongoDB Atlas.

Funcionalidades
GET: Obtener usuarios o un usuario específico.

POST: Crear un nuevo usuario.

PUT: Actualizar datos de un usuario existente.

DELETE: Eliminar un usuario.

Autenticación: JWT con OAuth para acceso seguro.

Base de datos: Conexión a MongoDB Atlas.

#Tecnologías utilizadas
Python 3.x

FastAPI

MongoDB Atlas

JWT (JSON Web Tokens)

OAuth2

Instalación
Clona el repositorio:

bash
Copiar
Editar
git clone https://github.com/MarcosTardy/mi-api-usuarios.git
cd mi-api-usuarios
Crea un entorno virtual (opcional pero recomendado):

bash
Copiar
Editar
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
Instala las dependencias:

bash
Copiar
Editar
pip install -r requirements.txt
Configura las variables de entorno para conectar con MongoDB Atlas y las claves JWT (ejemplo en .env).

Uso
Para iniciar la API:

bash
Copiar
Editar
uvicorn main:app --reload
La API estará disponible en http://localhost:8000.

Endpoints principales
GET /users — Obtener todos los usuarios

GET /users/{id} — Obtener usuario por ID

POST /users — Crear nuevo usuario

PUT /users/{id} — Actualizar usuario

DELETE /users/{id} — Eliminar usuario

Autenticación
La API utiliza JWT para proteger los endpoints. Se debe obtener un token válido para acceder a los recursos protegidos.

Contribuciones
¡Las contribuciones son bienvenidas! Puedes abrir issues o pull requests.

Licencia
Este proyecto está bajo licencia MIT.
