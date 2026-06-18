#Bases
from API.Routes.base import *
from Infrastructure.Repositories.base import Session, Depends, criar_sessao
from Application.base import verificar_permissao, verificar_token

#Exceptions
from Domain.exceptions import ExceptionGenerica, ExceptionHTTP

#Logs
from Infrastructure.Repositories.Registros.reLogs import salvar_log_bd


estoque_router = APIRouter(prefix='/estoque', tags=['estoque']) 

# OBS: CRIAÇÃO AUTOMÁTICA NA CRIAÇÃO DA FILIAL

# Listar 
@estoque_router.get('/')
async def listar_estoque(
    id: int | None=None,
    filial: int | None=None,
    ativo: bool | None=None,
    sessao:Session = Depends(criar_sessao), 
    ator=Depends(verificar_token)
    ):
    try:
        verificar_permissao(ator, 'estoque', 'listar')
        lista = exec_busca(id, filial, ativo, sessao, ator)
        salvar_log_bd('criar','variacao','id',variacao['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return lista

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Itens - Criar (EstoqueItens)
@estoque_router.post('{id}/itens/criar')
async def criar_estoque_itens(id: int, schema: ItemCriacaoSchema, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        validar_schema_estoqueitem_criar(schema)
        verificar_permissao(ator, 'estoque', 'criar item')
        estoque = verificar_estoque_existe(id, sessao)
        ingrediente = verificar_ingrediente_existe(schema.ingrediente, sessao)
        item = criar_estoque_itens_bd(id, schema, sessao)
        salvar_log_bd('criar','EstoqueItem','id',variacao['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return item

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Itens - Editar (EstoqueItens)
@estoque_router.post('{id}/itens/editar')
async def editar_estoque_itens(id: int, schema:ItemEdicaoSchema, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        verificar_permissao(ator, 'estoque', 'editar item')
        estoque = verificar_estoque_existe(id, sessao)
        item = verificar_item_existe(schema, sessao)
        item_editado = editar_estoque_itens_bd(id, schema, sessao)
        salvar_log_bd('criar','variacao','id',variacao['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return item_editado

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-