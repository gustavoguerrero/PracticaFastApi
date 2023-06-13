from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login") # Se le pasa la URL que se ancarga de la autenticacion

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str


users_db = {
    "mouredev":{
        "username": "mouredev",
        "full_name": "Braise Moure",
        "email": "brasmoure@mouredev.com",
        "disabled": False,
        "password": "123456"
    },

    "mouredev2":{
        "username": "mouredev2",
        "full_name": "Braise Moure 2",
        "email": "brasmoure2@mouredev.com",
        "disabled": True,
        "password": "123456"
    }
    
}

def searchUserDb(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def searchUser(username: str):
    if username in users_db:
        return User(**users_db[username])

async def current_user(token: str = Depends(oauth2)):
    user = searchUser(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="El password no es correcto", 
            headers={"WWWW-Authenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario Inactivo")

    return user

@app.post("/login")
async def login(form:OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    print(f'###############{user_db}##############')
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El usuario no es correcto")
    
    user = searchUser(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Contrasena incorrecta")

    return {"access_token": user.username , "token_type": "bearer"}

@app.get("/users/me")
async def me(user:User = Depends(current_user)):
    return user