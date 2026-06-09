from Application.base import *

#API - Schemas
from API.Schemas.usuario_schema import CriacaoSchema

from Infrastructure.Models.Persona.mUsuario import *
from Infrastructure.Repositories.reUsuario import *

async def validar_schema_usuario(schema: CriacaoSchema):
    if not schema.nome or not schema.email or not schema.senha:
        return False
    else:
        return True

async def verificar_token(email: str, senha: str, sessao:Session=Depends(criar_sessao)):
    usuario = sessao.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return {
            f'Não existe um usuário com email {email} no sistema'}
    
    