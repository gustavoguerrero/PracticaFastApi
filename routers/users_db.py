from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import userSchema
from db.client import db_client



router = APIRouter(prefix="/usersdb", 
                    tags=["users_db"],
                    responses = {status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})




users_list = []

@router.get('/')
async def users():
    return users_list

@router.get('/{id}')
async def user(id: int):
    return searchUser(id)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(searchUserByEmail(user.email))==User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND , detail="El usuario ya existe")

    userDict = dict(user)
    del userDict['id']

    id = db_client.local.users.insert_one(userDict).inserted_id

    newUser = userSchema(db_client.local.users.find_one({"_id":id})) 

    return User(**newUser)
        
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


def searchUserByEmail(email: str):

    try:
        user = db_client.local.users.find_one({"email": email}) 
        return User(**userSchema(user))
    except:
        return {"error": "Usuario no encontrado"}

def searchUser(id: int):
    return ""
