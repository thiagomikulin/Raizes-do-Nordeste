from API.Routes.base import *
from Infrastructure.Repositories.base import Session, Depends, criar_sessao
from Application.base import verificar_token, verificar_permissao
from Domain.exceptions import ExceptionHTTP, ExceptionGenerica
#logs
from Infrastructure.Repositories.Registros.reLogs import salvar_log_bd

#Recursos de ingrediente
from API.Schemas.Itens.sIngredientes import CriacaoSchema
from Application.Item.fIngrediente import verificar_schema_criacao_ingrediente
from Infrastructure.Repositories.Item.reIngrediente import verificar_ingrediente_existe, criar_ingrediente_db

ingrediente_router = APIRouter(prefix='/ingredientes', tags=['ingrediente'])

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Criar
@ingrediente_router.post('/criar')
async def criar_ingrediente(schema: CriacaoSchema, sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        verificar_schema_criacao_ingrediente(schema)
        verificar_permissao(ator, 'ingrediente', 'criar')
        verificar_ingrediente_existe(schema.nome, sessao)
        ingrediente = criar_ingrediente_db(schema, sessao)
        salvar_log_bd('criar','ingredientes','id',ingrediente['ingrediente']['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    return ingrediente

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Consultar
@ingrediente_router.get('/')
async def consulta_ingrediente():
    pass

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Editar
@ingrediente_router.put('/{id}')
async def editar_ingrediente(sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        salvar_log_bd('editar','variacao','id',ingrediente['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return     

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Ativar
@ingrediente_router.patch('/{id}/ativar')
async def ativar_ingrediente(sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        salvar_log_bd('criar','variacao','id',ingrediente['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return 

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Desativar
@ingrediente_router.patch('/{id}/desativar')
async def desativar_ingrediente(sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        salvar_log_bd('criar','variacao','id',ingrediente['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return 

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Alterar período 
@ingrediente_router.patch('/{id}/periodo')
async def alterar_periodo(sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        salvar_log_bd('criar','variacao','id',ingrediente['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return 
