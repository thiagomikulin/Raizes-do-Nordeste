from fastapi import APIRouter

#API - Schemas
from API.Schemas.usuario_schema import CriacaoSchema

#Infrastructure
from Infrastructure.dependencies import *

usuario_router = APIRouter(prefix='/usuarios', tags=['usuário'])

@usuario_router.post('/criar')
async def criar_usuario(schema: CriacaoSchema):
    """
    Cria um novo usuário
    """
    # Para o uso inicial do sistema, deve ser utilizado o usuário master
    return {"usuario":schema.email}
