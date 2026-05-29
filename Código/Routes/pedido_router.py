from fastapi import APIRouter

pedido_router = APIRouter(prefix='/pedido', tags=['pedido'])

@pedido_router.get('/novo')
async def novo_pedido():
    return {'pedido':1}