from Routes.base import *

ingrediente_router = APIRouter(prefix='ingredientes', tags=['ingrediente'])

# Criar
@ingrediente_router.post('/criar')
async def criar_ingredientr(schema: CriacaoSchema, session: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    pass

# Consultar

# Editar

# Ativar

# Desativar

# Alterar período 

