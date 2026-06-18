from API.Routes.base import *
from Application.base import verificar_permissao
from Domain.exceptions import ExceptionHTTP, ExceptionGenerica

log_router = APIRouter(prefix='/logs', tags=['log'])

# Consultar
@log_router.get('/')
async def listar_logs():
    try:
        verificar_permissao()
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return logs

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Salvar backup (complementar, caso dê tempo)