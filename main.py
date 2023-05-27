from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import products, users

app = FastAPI()

app.include_router(products.router)
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/')
async def root():
    return {"message": "Hola"}
