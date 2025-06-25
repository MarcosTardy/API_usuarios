from fastapi import APIRouter
router = APIRouter(prefix="/products", tags = ["product"], 
                   responses={404: {"message": "No encontrado"}})

products_list = ["Producto1", "Producto2", "Producto3"]
@router.get("/")
async def products():
    return products_list
@router.get("/{id}")
async def products(id:int):
    return products_list[id]