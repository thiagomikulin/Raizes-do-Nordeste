from API.Routes.base import *
from API.Schemas.Empresa.sFilial import *

filial_router = APIRouter(prefix='/filiais', tags=['filial'])

@filial_router.post('/criar')
async def criar_filial(schema: CriacaoSchema, sessao:Session = Depends(criar_sessao)):
    return True