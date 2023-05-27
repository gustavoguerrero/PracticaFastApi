from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/products", 
                    tags=["products"],
                    responses={404: {"message": "No encontrado"}})

class Product(BaseModel):
    id: int
    name: str
    

products_list = [
        Product(id=1, name="Producto 1"),
        Product(id=2, name= "Producto 2"),
        Product(id=3, name= "Producto 3")
    ]


@router.get("/")
async def products():
    return products_list

@router.get('/{id}')
async def products(id: int):
    return searchProduct(id)

'''
###DEPRECATED###
@router.get('/productquery/')
async def user(id: int):
    return searchProduct(id)
'''

def searchProduct(id: int):
    products = filter(lambda products: products.id == id, products_list)
    try:
        return list(products)[0]    
    except:
        return {"error": "Usuario no encontrado"}
