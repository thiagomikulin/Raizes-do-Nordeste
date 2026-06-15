from fastapi import APIRouter

produto_router = APIRouter(prefix='/produto', tags=['produto'])

# Criar

# Listar
@produto_router.get('/produto')
async def get_produto():
    return {'produto':'Acarajé'}

# Editar

# Consultar Quantidade

# Desativar

# Ativar