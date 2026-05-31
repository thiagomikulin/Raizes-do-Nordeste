from fastapi import APIRouter

usuario_router = APIRouter(prefix='/usuario', tags=['usuário'])

@usuario_router.post('/criar')
async def criar_usuario():
    """
    Cria um novo usuário
    """
    # Para o uso inicial do sistema, deve ser utilizado o usuário master
