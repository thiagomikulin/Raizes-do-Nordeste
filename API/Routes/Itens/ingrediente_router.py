from API.Routes.base import *
from Infrastructure.Repositories.base import Session, Depends, criar_sessao
from Application.base import verificar_token, verificar_permissao
from Domain.__exceptions__ import ExceptionHTTP, ExceptionGenerica

from Application.chamada_rota import ativar_entidade, criar_entidade, desativar_entidade, editar_entidade, visualizar_entidade

#logs
from Infrastructure.Repositories.Registros.reLogs import salvar_log_bd

#Recursos de ingrediente
from API.Schemas.Itens.sIngredientes import CriacaoSchema, EdicaoSchema
from Application.Item.fIngrediente import verificar_schema_criacao_ingrediente
from Infrastructure.Repositories.Item.reIngrediente import verificar_ingrediente_existe, criar_ingrediente_db
from Infrastructure.Models.Item.mIngrediente import Ingrediente, PeriodoAno

ingrediente_router = APIRouter(prefix='/ingredientes', tags=['Itens - Ingredientes'])

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Criar
@ingrediente_router.post('/criar')
async def criar_ingrediente(schema: CriacaoSchema, sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        ingrediente = criar_entidade(Ingrediente, schema, ator, sessao, campo_verificacao=['nome'])
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    return ingrediente

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Consultar
@ingrediente_router.get('/')
async def consulta_ingrediente(
    id: int | None=None,
    nome: str | None=None,
    periodo: PeriodoAno | None=None,
    sessao:Session = Depends(criar_sessao), 
    ator=Depends(verificar_token)
):
    dict_campos = {
        "id":id,
        "nome":nome,
        "periodo":periodo
    }
    try:
        lista = visualizar_entidade(Ingrediente, sessao, ator, dict_campos)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    return lista

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Editar
@ingrediente_router.put('/{id}')
async def editar_ingrediente(id: int, schema: EdicaoSchema, sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        ingrediente_alterado = editar_entidade(id, Ingrediente, schema, ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return ingrediente_alterado    

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Ativar
@ingrediente_router.patch('/{id}/ativar')
async def ativar_ingrediente(id: int, sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        ingrediente_ativo = ativar_entidade(Ingrediente, ator, id, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return ingrediente_ativo

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Desativar
@ingrediente_router.patch('/{id}/desativar')
async def desativar_ingrediente(id: int, sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        ingrediente_desativo = desativar_entidade(Ingrediente, ator, id, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return ingrediente_desativo

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
