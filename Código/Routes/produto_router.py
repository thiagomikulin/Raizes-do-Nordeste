from fastapi import APIRouter

produto_router = APIRouter(prefix='/produto', tags=['produto'])

@produto_router.get('/produto')
async def get_produto():
    return {'produto':'Acarajé'}