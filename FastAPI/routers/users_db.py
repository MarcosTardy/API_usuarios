from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.models.user_class import User
from pymongo import MongoClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.schemas.user import user_schema, users_schema
from bson import ObjectId
from db.client import users_collection

db_client = MongoClient()

router = APIRouter(prefix = "/userdb", 
                   tags = ["userdb"], 
                   responses = {status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

@router.get("/")
async def root():
    return "Hola"
    
#users_list = []

@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.local.users.find())

#Path
@router.get("/{id}")
async def users(id):
    return search_user("_id", ObjectId(id))

#Query
@router.get("/userquery/")
async def users(id):
    return search_user("_id", ObjectId(id))

@router.post("/", response_model= User, status_code=201)
async def user(user: User):
    if type (search_user("email", user.email)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe.")
    user_dict = dict(user)
    del user_dict["id"]
    
    id = users_collection.insert_one(user_dict).inserted_id
    
    new_user = user_schema(users_collection.find_one({"_id": id}))
    
    return User(**new_user)

@router.put("/", response_model = User)
async def user(user: User):
    user_dict = dict(user)
    del user_dict["id"]
    
    try:
        result = users_collection.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict
        )
        if not result:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se ha actualizado el usuario. Error: {str(e)}")
    
    updated_user = search_user("_id", ObjectId(user.id))
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuario actualizado no encontrado.")
    
    return updated_user
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    found = users_collection.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        raise HTTPException(status_code=404, detail="No se ha eliminado.")
      
def search_user(field: str, key):
    user = users_collection.find_one({field: key})
    if user:
        return User(**user_schema(user))
    return None