from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 60
SECRET = "vggbbgbgrret5tgg656"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

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
        "password": "$2a$12$HzLi4eblVehCMf4lcrCtY.1FugwQaPxN9qASQeNkaCt4OZc5c4g2u"
    },
    "MikeDioso": {
        "username": "MikeDioso",
        "full_name": "Mike Dioso",
        "email": "vanhalen_fan@gmail.com",
        "disabled": True,
        "password": "$2a$12$.HNF3VTy.OZp/XmVBXV6du4LjcDd/oi.5USlcl0poanN6EeLwZL.W"
    }
}
def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])
    
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username) 
    if not user_db:
        raise HTTPException(
            status_code=400, detail="El usuario no es correcto")
    user = search_user_db(form.username)
        
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=400, detail ="La contraseña no es correcta")      
    access_token = {"sub":user.username, 
                    "exp":datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)
                    }
    
    return {"acces_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

async def auth_user(token: str = Depends(oauth2)):
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail= "Credenciales de autenticación invalidas.", 
                headers={"WWW-Authenticate":"Bearer"})
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail= "Credenciales de autenticación invalidas.", 
            headers={"WWW-Authenticate":"Bearer"})
    return search_user(username)
    
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail= "Usuario inactivo.")
    return user

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user