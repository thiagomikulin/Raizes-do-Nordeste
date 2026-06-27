from API.Routes.base import *
from Application.base import verificar_permissao, verificar_token
from Application.chamada_rota import visualizar_entidade
from Infrastructure.Repositories.base import Session, Depends, criar_sessao
from Infrastructure.Models.Registros.mLogs import Tabelas, Acoes
from Infrastructure.Models.base import TipoLogin
from Domain.__exceptions__ import ExceptionHTTP, ExceptionGenerica

from Infrastructure.Models.Registros.mLogs import Log

log_router = APIRouter(prefix='/logs', tags=['Logs'])

# Consultar
@log_router.get('/')
async def listar_logs(
    acao: Acoes | None=None,
    tabela: Tabelas | None=None,
    id_modificado: int | None=None,
    campo: str | None=None,
    tipo_pessoa: TipoLogin | None=None,
    id_pessoa: int | None=None,
    sessao:Session = Depends(criar_sessao), 
    ator=Depends(verificar_token)
):
    dict_campos = {
        "acao":acao,
        "tabela":tabela,
        "id_modificado":id_modificado,
        "campo":campo,
        "tipo_pessoa":tipo_pessoa,
        "id_pessoa":id_pessoa
    }
    try:
        logs = visualizar_entidade(Log,sessao, ator, dict_campos )
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return logs

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Salvar backup (complementar, caso dê tempo)