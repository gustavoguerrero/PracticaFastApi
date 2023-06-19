from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 
SECRET = "530344f19a2bafdf3c42bcd599087f03dbc116254564d8a59f7e938cf902e4cb"

router = APIRouter(prefix="/login", 
                    tags=["login"],
                    responses={404: {"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypth = CryptContext(schemes=['bcrypt'])

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
        "password": "$2a$12$tHvkIzJX6HneHIPSrC91xO2OBxQgYnl1YtAzTSUifrmYKLSyOjCUK"

    },

    "mouredev2":{
        "username": "mouredev2",
        "full_name": "Braise Moure 2",
        "email": "brasmoure2@mouredev.com",
        "disabled": True,
        "password": "$2a$12$tHvkIzJX6HneHIPSrC91xO2OBxQgYnl1YtAzTSUifrmYKLSyOjCUK"
    }
    
}

def searchUserDb(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def searchUser(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token:str = Depends(oauth2)):

    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="El password no es correcto", 
            headers={"WWWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
        
    except JWTError:
        raise exception
    
    return searchUser(username)
    

async def current_user(user : User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario Inactivo")
    return user

@router.post("/login")
async def login(form:OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El usuario no es correcto")
    
    user = searchUserDb(form.username)
    if not crypth.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Contrasena incorrecta")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    
    access_token = {
        "sub": user.username,
        "exp": expire
    }

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM) , "token_type": "bearer"}


@router.get("/users/me")
async def me(user:User = Depends(current_user)):
    return user