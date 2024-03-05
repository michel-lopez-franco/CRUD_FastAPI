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


