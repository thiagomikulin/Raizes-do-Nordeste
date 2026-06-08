from API.Routes.base import *

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
    if not schema.nome or not schema.email or not schema.senha:
        raise ExceptionHTTP(
            code=400, 
            error='CAMPOS PREENCHIDOS INCORRETAMENTE',
            message="Os campos não foram preenchidos corretamente! Verifique e tente novamente",
            detail=[{"field":attr, "issue":"required"} for attr, val in schema.__dict__.items() if not val], #Retorna o atributo na lista de atributos e valores se o valor não existir
            timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            path='/usuarios/criar'
        )
    
        
