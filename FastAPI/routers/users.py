from fastapi import APIRouter, HTTPException 
from pydantic import BaseModel
from pydantic import BaseModel
router = APIRouter(tags = ["user"])

@router.get("/")
async def root():
    return "Hola"

class User(BaseModel):
    id : int
    name: str
    surname: str
    url: str
    age: int
users_list = [User(id = 1, name = "Marcos", surname = "Tardy", url = "https://mtardy.com", age = 22),
              User(id = 2, name = "Renato", surname = "Sánchez", url = "https://rsanchez.com", age = 30),
              User(id = 3, name = "Mike", surname = "Dioso", url = "https://mdioso.com", age = 220)]

@router.get("/users")
async def users():
    return users_list

#Path
@router.get("/user/{id}")
async def users(id: int):
    return search_user(id)

#Query
@router.get("/userquery/")
async def users(id: int):
    return search_user(id)

@router.post("/user/", response_model= User, status_code=201)
async def user(user: User):
    if type (search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe.")
    users_list.append(user)
    return user
    
@router.put("/user/")
async def user(user: User):
    found = False
    for i, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[i] = user
            found = True
    if not found:
        raise HTTPException(status_code=404, detail="El usuario no existe.")

@router.delete("/user/{id}")
async def user(id: int):
    found = False
    for i, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[i]
            found = True
    if not found:
        raise HTTPException(status_code=404, detail="No se ha econtrado un usuario con este ID.")
      
def search_user(id: int):
    usuarios = filter(lambda user: user.id == id, users_list ) 
    try: 
        return list(usuarios)[0]
    except: 
        raise HTTPException(status_code=404, detail="No se ha podido encotrar este usuario.")