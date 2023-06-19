from fastapi import APIRouter, HTTPException
from typing import Union
from db.models.user import User

router = APIRouter(prefix="/usersdb", 
                    tags=["users_db"],
                    responses={404: {"message": "No encontrado"}})




users_list = []

@router.get('/')
async def users():
    return users_list

@router.get('/{id}')
async def user(id: int):
    return searchUser(id)

'''
## DEPRECATED ##
@router.get('/userquery/')
async def user(id: int):
    return searchUser(id)
'''

@router.post("/", response_model=User, status_code=201)
async def user(user: User):
    if type(searchUser(user.id))==User:
        raise HTTPException(status_code=204, detail="El usuario ya existe")

    users_list.append(user)
    return user
        
@router.put("/")
async def user(user: User):
    found = False

    for index, savedUser in enumerate(users_list) :
        if savedUser.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error": "Usuario no actualizado"}
    else:
        return {"exito": "Usuario actualizado"}

@router.delete("/{id}")
async def user(id: int):
    found = False

    for index, savedUser in enumerate(users_list) :
        if savedUser.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"error": "Usuario no encontrado"}
    else:
        return {"exito": "Usuario eliminado"}


def searchUser(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]    
    except:
        return {"error": "Usuario no encontrado"}

