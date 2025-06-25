from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException 

router = APIRouter() 

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "Brauro": {
        "username": "Brauro",
        "full_name": "Marcos Tardy",
        "email": "marcost@gmail.com",
        "disabled": False,
        "password": "123456"
    },
    "MikeDioso": {
        "username": "MikeDioso",
        "full_name": "Mike Dioso",
        "email": "vanhalen_fan@gmail.com",
        "disabled": True,
        "password": "654321"
    }
}
    
def search_user(username:str):
    if username in users_db:
        return UserDB(**users_db[username])

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail= "Credenciales de autenticación invalidas.", 
            headers={"WWW-Authenticate":"Bearer"}
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail= "Usuario inactivo.")
    return user
      
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username) 
    if not user_db:
        raise HTTPException(
            status_code=400, detail="El usuario no es correcto")
    user = search_user(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=400, detail ="La contraseña no es correcta")
    
    return {"acces_token": user.username, "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user