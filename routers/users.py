from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Union

router = APIRouter(prefix="/users", 
                    tags=["users"],
                    responses={404: {"message": "No encontrado"}})


class User(BaseModel):
    id: int
    name: str
    surname: str
    doc: str
    age: int

users_list = [User(id=1, name="Brais", surname="Moure", age="33", doc="UY-DOC-1"),
        User(id=2, name= "Jhon",surname=  "Doe", age= "33", doc="UY-DOC-2")
    ]

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

@router.post("/ingresar", response_model=User, status_code=201)
async def user(user: User):
    if type(searchUser(user.id))==User:
        raise HTTPException(status_code=204, detail="El usuario ya existe")

    users_list.append(user)
    return user
        
@router.put("/modificar")
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

@router.delete("/borrar/{id}")
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

