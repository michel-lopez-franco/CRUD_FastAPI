# Un Ejemplo de CRUD realizado con python y FastAPI

Una pequeña guia 
https://mulberry-kumquat-db1.notion.site/Crear-una-API-REST-fa31c34675624860b14bf31f0f18b218?pvs=4


# Crear una API REST

## API VS API REST

La diferencia entre una API (Interfaz de Programación de Aplicaciones) y una API REST (Transferencia de Estado Representacional) radica principalmente en el estilo arquitectónico y en cómo se comunican e intercambian datos entre distintas aplicaciones de software.

1. **API (Interfaz de Programación de Aplicaciones):** Es un conjunto de reglas, protocolos y herramientas para construir software y aplicaciones. Permite que diferentes aplicaciones se comuniquen entre sí sin necesidad de saber cómo están implementadas internamente. Las APIs pueden ser diseñadas utilizando diferentes arquitecturas y protocolos, como SOAP (Simple Object Access Protocol), RPC (Remote Procedure Call), entre otros.
2. **API REST (Transferencia de Estado Representacional):** Es un estilo arquitectónico de diseño de APIs que utiliza el protocolo HTTP para hacer llamadas a servicios web. Se basa en principios como el uso de métodos HTTP (GET, POST, PUT, DELETE, etc.), la comunicación sin estado, y la posibilidad de utilizar formatos de mensaje como JSON o XML. Las APIs REST están orientadas a recursos, lo que significa que el acceso y la manipulación de los datos se realizan a través de la representación de estos recursos. Uno de los aspectos clave de REST es que es agnóstico respecto al formato de los datos, permitiendo flexibilidad en la forma en que se transmiten los datos.

En resumen, la principal diferencia es que todas las APIs REST son APIs, pero no todas las APIs son REST. REST es un conjunto específico de principios que guían el diseño y desarrollo de APIs, enfocado en la simplicidad, el rendimiento, y la escalabilidad, mientras que el término "API" es más general y puede abarcar una mayor variedad de protocolos y estilos de arquitectura.

https://aws.amazon.com/es/what-is/restful-api/

[https://appmaster.io/blog/what-rest-api-and-how-it-differs-other-types#:~:text=from other APIs.-,Defining REST API,-REST is an](https://appmaster.io/blog/what-rest-api-and-how-it-differs-other-types#:~:text=from%20other%20APIs.-,Defining%20REST%20API,-REST%20is%20an)

# CRUD

CRUD es un acrónimo en inglés para las cuatro operaciones básicas utilizadas en bases de datos y en el desarrollo de aplicaciones para manipular datos persistentes. Las letras C, R, U, y D se refieren a las siguientes operaciones:

1. **Create (Crear):** Esta operación hace referencia a la capacidad de añadir nuevos registros o datos a la base de datos. Por ejemplo, añadir un nuevo usuario a una lista de usuarios.
2. **Read (Leer):** Se refiere a la capacidad de leer, consultar o recuperar datos existentes. Esto incluye buscar y obtener registros o datos específicos de la base de datos, como visualizar la información de un usuario específico.
3. **Update (Actualizar):** Esta operación permite modificar datos existentes en la base de datos. Por ejemplo, cambiar la dirección de correo electrónico de un usuario.
4. **Delete (Eliminar):** Se refiere a la capacidad de eliminar datos existentes. Esto puede implicar borrar un registro completo, como eliminar una cuenta de usuario.

El concepto de CRUD es fundamental en el diseño de sistemas que requieren interacción con bases de datos o cualquier otro almacenamiento de datos persistente, ya que estas cuatro operaciones constituyen la esencia de la gestión de datos. La simplicidad y universalidad del modelo CRUD facilitan la comprensión y el diseño de sistemas eficaces para el manejo de datos. Las aplicaciones que implementan funcionalidades CRUD permiten a los usuarios gestionar datos de manera efectiva, realizando operaciones básicas sin necesidad de conocimientos complejos sobre la estructura subyacente de la base de datos.

# Ejemplo utilizando fastAPI

Creamos un entorno en conda (necesitamos tener anaconda previamente instalada)

https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

`conda create -n fastAPI python=3.12`

Instalamos paquetes que vamos a necesitar 

pip install fastapi

pip install "uvicorn[standard]”

pip install cryptography

https://fastapi.tiangolo.com/#installation

Crea un archivo `main.py` con

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

Ejecuta con 

```bash
uvicorn main:app
```

**Interactive API docs**

 http://127.0.0.1:8000/docs

Lecturas recomendadas

- https://fastapi.tiangolo.com/python-types/
- https://fastapi.tiangolo.com/async/
- https://fastapi.tiangolo.com/tutorial/first-steps/

Si hacemos un cambio no se verea modificado, para no estar cerrando y estar ejecutandolo de nuevo añadimos la propiedad —reload

```bash
uvicorn main:app --reload
```

```bash
uvicorn (archivo):(nombre de la instanca de FastAPI) --reload
```

## No todas las rutas (path) deben de estar en el mismo archivo Gestion de datos y rutas modulares

Genera una carpeta llamda “routes” y añadimos un archivo llamado user.py 

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/e11c49a6-44d7-4cdf-91f3-1e4e6ab08d3e/44056343-aa1b-4771-aa25-4d10b9f71879/Untitled.png)

user.py

```python
from fastapi import APIRouter

user = APIRouter()

@user.get("/users")
def binvenida():
    return {"bienvenida": "Hola a fastapi en users"}

```

main.py

```python
from fastapi import FastAPI
from routes.user import user

app = FastAPI()

app.include_router(user)

@app.get("/")
async def root():
    return {"message": "Hello World"}

```

```bash
uvicorn main:app --reload
```

vamos a http://127.0.0.1:8000/docs

# Ejemplo practico

Ahora vamos a implementar las operaciones CRUD

Create, Read, Update, Delete

- Create -> POST
- Read -> GET
- Update -> PUT
- Delete -> DELETE

En [user.py](http://user.py) agregar lo siguiente 

```python
#Genermaos una lista como si fuera una base de datos posts
posts = []
```

Para seguir las buenas prácticas de programación, especificaremos los tipos de datos que contendrá nuestro arreglo. Para esto utilizamos la biblioteca de Python llamada pydantic, que nos ayudará a definir un esquema de tipo de datos.

```python
#Para seguir las buenas prácticas de programación, especificaremos los tipos de datos que contendrá nuestro arreglo. Para esto utilizamos la biblioteca de Python llamada pydantic, que nos ayudará a definir un esquema de tipo de datos.
class Post(BaseModel):
    id: str = str(uuid()) #Generamos un id único para cada post
    username: str
    email: str
    password: str
    active: bool = True

```

Generamos un id único para cada post con uuid.

Las librerias serian from pydantic import BaseModel y from uuid import uuid4 as uuid

```python
from fastapi import FastAPI
from routes.user import user
from pydantic import BaseModel
from uuid import uuid4 as uuid
```

Ahora, crearemos una ruta para agregar un nuevo post a nuestra lista de posts. Para esto, utilizaremos el método POST de HTTP.

```python
# Ahora, crearemos una ruta para agregar un nuevo post a nuestra lista de posts. Para esto, utilizaremos el método POST de HTTP.
@user.post("/posts")
def create_posts(post: Post):
    post.id = str(uuid())
    posts.append(dict(post))
    return posts[-1]
```

user.py

```python
from fastapi import APIRouter
from pydantic import BaseModel
from uuid import uuid4 as uuid

user = APIRouter()

@user.get("/users")
def binvenida():
    return {"bienvenida": "Hola a fastapi en users"}

#Genermaos una lista como si fuera una base de datos posts
posts = []

#Para seguir las buenas prácticas de programación, especificaremos los tipos de datos que contendrá nuestro arreglo. Para esto utilizamos la biblioteca de Python llamada pydantic, que nos ayudará a definir un esquema de tipo de datos.
class Post(BaseModel):
    id: str = str(uuid()) #Generamos un id único para cada post
    username: str
    email: str
    password: str
    active: bool = True

# Ahora, crearemos una ruta para mostrar todos los posts que tenemos en nuestra lista. Para esto, utilizaremos el método GET de HTTP.
@user.get("/posts")
def get_posts():
    return posts

# Ahora, crearemos una ruta para agregar un nuevo post a nuestra lista de posts. Para esto, utilizaremos el método POST de HTTP.
@user.post("/posts")
def create_posts(post: Post):
    post.id = str(uuid())
    posts.append(dict(post))
    return posts[-1]
```

main.py

```python
from fastapi import FastAPI
from routes.user import user

app = FastAPI()

app.include_router(user)

@app.get("/")
async def root():
    return {"message": "Hello World"}

```

Ejecutamos de nuevo

```bash
uvicorn main:app --reload
```

Ahora, crearemos una ruta para leer un post de nuestra lista de posts. Para esto, utilizaremos el método GET de HTTP.

```python
@user.get("/posts/{user_id}")
def get_posts(user_id: str):
    for post in posts:
        if post["id"] == user_id:
            return post
    return "No se encontro el usuario"
```

user.py

```python
from fastapi import APIRouter
from pydantic import BaseModel
from uuid import uuid4 as uuid

user = APIRouter()

@user.get("/users")
def binvenida():
    return {"bienvenida": "Hola a fastapi en users"}

# Ahora vamos a implementar las operaciones CRUD
# Create, Read, Update, Delete
# Create -> POST
# Read -> GET
# Update -> PUT
# Delete -> DELETE

#Genermaos una lista como si fuera una base de datos posts
posts = []

#Para seguir las buenas prácticas de programación, especificaremos los tipos de datos que contendrá nuestro arreglo. Para esto utilizamos la biblioteca de Python llamada pydantic, que nos ayudará a definir un esquema de tipo de datos.
class Post(BaseModel):
    id: str = str(uuid()) #Generamos un id único para cada post
    username: str
    email: str
    password: str
    active: bool = True

# Ahora, crearemos una ruta para mostrar todos los posts que tenemos en nuestra lista. Para esto, utilizaremos el método GET de HTTP.
@user.get("/posts")
def get_posts():
    return posts

# Ahora, crearemos una ruta para agregar un nuevo post a nuestra lista de posts. Para esto, utilizaremos el método POST de HTTP.
# Create -> POST
@user.post("/posts")
def create_posts(post: Post):
    post.id = str(uuid())
    posts.append(dict(post))
    return posts[-1]

# Ahora, crearemos una ruta para leer un post de nuestra lista de posts. Para esto, utilizaremos el método GET de HTTP.
# Read -> GET
@user.get("/posts/{user_id}")
def get_posts(user_id: str):
    for post in posts:
        if post["id"] == user_id:
            return post
    return "No se encontro el usuario"
```

Ahora, crearemos una ruta para actualizar un post de nuestra lista de posts. Para esto, utilizaremos el método PUT de HTTP.

```python
# Ahora, crearemos una ruta para actualizar un post de nuestra lista de posts. Para esto, utilizaremos el método PUT de HTTP.
# Update -> PUT
@user.put("/posts/{user_id}")
def update_posts(user_id: str,updatePost: Post):
    for index,post in enumerate(posts):
        if post["id"] == user_id:
            posts[index]["username"] = updatePost.username
            posts[index]["email"] = updatePost.email
            posts[index]["password"] = updatePost.password
            posts[index]["active"] = updatePost.active
            return "Usuario correctamente actualizado"
    return "No se encontro el usuario"
```

user.py

```python
from fastapi import APIRouter
from pydantic import BaseModel
from uuid import uuid4 as uuid

user = APIRouter()

@user.get("/users")
def binvenida():
    return {"bienvenida": "Hola a fastapi en users"}

# Ahora vamos a implementar las operaciones CRUD
# Create, Read, Update, Delete
# Create -> POST
# Read -> GET
# Update -> PUT
# Delete -> DELETE

#Genermaos una lista como si fuera una base de datos posts
posts = []

#Para seguir las buenas prácticas de programación, especificaremos los tipos de datos que contendrá nuestro arreglo. Para esto utilizamos la biblioteca de Python llamada pydantic, que nos ayudará a definir un esquema de tipo de datos.
class Post(BaseModel):
    id: str = str(uuid()) #Generamos un id único para cada post
    username: str
    email: str
    password: str
    active: bool = True

# Ahora, crearemos una ruta para mostrar todos los posts que tenemos en nuestra lista. Para esto, utilizaremos el método GET de HTTP.
@user.get("/posts")
def get_posts():
    return posts

# Ahora, crearemos una ruta para agregar un nuevo post a nuestra lista de posts. Para esto, utilizaremos el método POST de HTTP.
# Create -> POST
@user.post("/posts")
def create_posts(post: Post):
    post.id = str(uuid())
    posts.append(dict(post))
    return posts[-1]

# Ahora, crearemos una ruta para leer un post de nuestra lista de posts. Para esto, utilizaremos el método GET de HTTP.
# Read -> GET
@user.get("/posts/{user_id}")
def get_posts(user_id: str):
    for post in posts:
        if post["id"] == user_id:
            return post
    return "No se encontro el usuario"

# Ahora, crearemos una ruta para actualizar un post de nuestra lista de posts. Para esto, utilizaremos el método PUT de HTTP.
# Update -> PUT
@user.put("/posts/{user_id}")
def update_posts(user_id: str,updatePost: Post):
    for index,post in enumerate(posts):
        if post["id"] == user_id:
            posts[index]["username"] = updatePost.username
            posts[index]["email"] = updatePost.email
            posts[index]["password"] = updatePost.password
            posts[index]["active"] = updatePost.active
            return "Usuario correctamente actualizado"
    return "No se encontro el usuario"
```

Ahora, crearemos una ruta para eliminar un post de nuestra lista de posts. Para esto, utilizaremos el método DELETE de HTTP.

```python
# Ahora, crearemos una ruta para eliminar un post de nuestra lista de posts. Para esto, utilizaremos el método DELETE de HTTP.
# Delete -> DELETE
@user.delete("/posts/{user_id}")
def delete_posts(user_id: str):
    for index,post in enumerate(posts):
        if post["id"] == user_id:
            posts.pop(index)
            return "Usuario correctamente eliminado"
    return "No se encontro el usuario"
```

user.py

```python
from fastapi import APIRouter
from pydantic import BaseModel
from uuid import uuid4 as uuid

user = APIRouter()

@user.get("/users")
def binvenida():
    return {"bienvenida": "Hola a fastapi en users"}

# Ahora vamos a implementar las operaciones CRUD
# Create, Read, Update, Delete
# Create -> POST
# Read -> GET
# Update -> PUT
# Delete -> DELETE

#Genermaos una lista como si fuera una base de datos posts
posts = []

#Para seguir las buenas prácticas de programación, especificaremos los tipos de datos que contendrá nuestro arreglo. Para esto utilizamos la biblioteca de Python llamada pydantic, que nos ayudará a definir un esquema de tipo de datos.
class Post(BaseModel):
    id: str = str(uuid()) #Generamos un id único para cada post
    username: str
    email: str
    password: str
    active: bool = True

# Ahora, crearemos una ruta para mostrar todos los posts que tenemos en nuestra lista. Para esto, utilizaremos el método GET de HTTP.
@user.get("/posts")
def get_posts():
    return posts

# Ahora, crearemos una ruta para agregar un nuevo post a nuestra lista de posts. Para esto, utilizaremos el método POST de HTTP.
# Create -> POST
@user.post("/posts")
def create_posts(post: Post):
    post.id = str(uuid())
    posts.append(dict(post))
    return posts[-1]

# Ahora, crearemos una ruta para leer un post de nuestra lista de posts. Para esto, utilizaremos el método GET de HTTP.
# Read -> GET
@user.get("/posts/{user_id}")
def get_posts(user_id: str):
    for post in posts:
        if post["id"] == user_id:
            return post
    return "No se encontro el usuario"

# Ahora, crearemos una ruta para actualizar un post de nuestra lista de posts. Para esto, utilizaremos el método PUT de HTTP.
# Update -> PUT
@user.put("/posts/{user_id}")
def update_posts(user_id: str,updatePost: Post):
    for index,post in enumerate(posts):
        if post["id"] == user_id:
            posts[index]["username"] = updatePost.username
            posts[index]["email"] = updatePost.email
            posts[index]["password"] = updatePost.password
            posts[index]["active"] = updatePost.active
            return "Usuario correctamente actualizado"
    return "No se encontro el usuario"

# Ahora, crearemos una ruta para eliminar un post de nuestra lista de posts. Para esto, utilizaremos el método DELETE de HTTP.
# Delete -> DELETE
@user.delete("/posts/{user_id}")
def delete_posts(user_id: str):
    for index,post in enumerate(posts):
        if post["id"] == user_id:
            posts.pop(index)
            return "Usuario correctamente eliminado"
    return "No se encontro el usuario"

```

Vamos a encriptar la contraseña para guardarla. utilizando Fernet

```python
from cryptography.fernet import Fernet
```

generamos una clave

```python
key = Fernet.generate_key()
fernet = Fernet(key)
```

Cada peticion post a posts encriptamos el password

```python
    encrypted_password = fernet.encrypt(post.password.encode())
    post.password = encrypted_password
```

Quedaria asi el metodo create_posts

```python
@user.post("/posts")
def create_posts(post: Post):
    post.id = str(uuid())
    encrypted_password = fernet.encrypt(post.password.encode())
    post.password = encrypted_password
    posts.append(dict(post))
    return posts[-1]
```

y en el metodo update_post 

modificamos 

posts[index]["password"] = updatePost.password 

por 

encrypted_password = fernet.encrypt(post.password.encode())
posts[index]["password"] = encrypted_password

```python
@user.put("/posts/{user_id}")
def update_posts(user_id: str,updatePost: Post):
    for index,post in enumerate(posts):
        if post["id"] == user_id:
            posts[index]["username"] = updatePost.username
            posts[index]["email"] = updatePost.email
            encrypted_password = fernet.encrypt(post.password.encode())
            posts[index]["password"] = encrypted_password
            posts[index]["active"] = updatePost.active
            return "Usuario correctamente actualizado"
    return "No se encontro el usuario"
```

user.py

```python
from fastapi import APIRouter
from pydantic import BaseModel
from uuid import uuid4 as uuid
from cryptography.fernet import Fernet

user = APIRouter()

@user.get("/users")
def binvenida():
    return {"bienvenida": "Hola a fastapi en users"}

key = Fernet.generate_key()
fernet = Fernet(key)

# Ahora vamos a implementar las operaciones CRUD
# Create, Read, Update, Delete
# Create -> POST
# Read -> GET
# Update -> PUT
# Delete -> DELETE

#Genermaos una lista como si fuera una base de datos posts
posts = []

#Para seguir las buenas prácticas de programación, especificaremos los tipos de datos que contendrá nuestro arreglo. Para esto utilizamos la biblioteca de Python llamada pydantic, que nos ayudará a definir un esquema de tipo de datos.
class Post(BaseModel):
    id: str = str(uuid()) #Generamos un id único para cada post
    username: str
    email: str
    password: str
    active: bool = True

# Ahora, crearemos una ruta para mostrar todos los posts que tenemos en nuestra lista. Para esto, utilizaremos el método GET de HTTP.
@user.get("/posts")
def get_posts():
    return posts

# Ahora, crearemos una ruta para agregar un nuevo post a nuestra lista de posts. Para esto, utilizaremos el método POST de HTTP.
# Create -> POST
@user.post("/posts")
def create_posts(post: Post):
    post.id = str(uuid())
    encrypted_password = fernet.encrypt(post.password.encode())
    post.password = encrypted_password
    posts.append(dict(post))
    return posts[-1]

# Ahora, crearemos una ruta para leer un post de nuestra lista de posts. Para esto, utilizaremos el método GET de HTTP.
# Read -> GET
@user.get("/posts/{user_id}")
def get_posts(user_id: str):
    for post in posts:
        if post["id"] == user_id:
            return post
    return "No se encontro el usuario"

# Ahora, crearemos una ruta para actualizar un post de nuestra lista de posts. Para esto, utilizaremos el método PUT de HTTP.
# Update -> PUT
@user.put("/posts/{user_id}")
def update_posts(user_id: str,updatePost: Post):
    for index,post in enumerate(posts):
        if post["id"] == user_id:
            posts[index]["username"] = updatePost.username
            posts[index]["email"] = updatePost.email
            encrypted_password = fernet.encrypt(post.password.encode())
            posts[index]["password"] = encrypted_password
            posts[index]["active"] = updatePost.active
            return "Usuario correctamente actualizado"
    return "No se encontro el usuario"

# Ahora, crearemos una ruta para eliminar un post de nuestra lista de posts. Para esto, utilizaremos el método DELETE de HTTP.
# Delete -> DELETE
@user.delete("/posts/{user_id}")
def delete_posts(user_id: str):
    for index,post in enumerate(posts):
        if post["id"] == user_id:
            posts.pop(index)
            return "Usuario correctamente eliminado"
    return "No se encontro el usuario"

```
