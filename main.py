from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import products, users, basic_auth_users, jwt_auth_users, users_db

app = FastAPI()

app.include_router(products.router)
app.include_router(users.router)
app.include_router(users_db.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/')
async def root():
    return {"message": "Hola"}
