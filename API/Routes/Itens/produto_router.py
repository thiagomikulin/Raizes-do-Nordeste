from API.Routes.base import APIRouter
from Application.base import verificar_permissao, verificar_token
from Infrastructure.Repositories.base import Session, Depends, criar_sessao
from Domain.exceptions import ExceptionHTTP, ExceptionGenerica
from Infrastructure.Repositories.Registros.reLogs import salvar_log_bd

from API.Schemas.Itens.sProdutos import CriacaoSchema
from Application.Item.fProduto import verificar_schema_criacao_produto


produto_router = APIRouter(prefix='/produto', tags=['produto'])

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Criar
@produto_router.post('/criar')
async def criar_produto(schema: CriacaoSchema, sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        verificar_schema_criacao_produto(schema)
        verificar_permissao(ator, 'produto', 'criar')
        verificar_produto_existe(schema.nome, sessao)
        produto = criar_produto_db(schema, sessao)
        salvar_log_bd('criar','variacao','id',variacao['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return produto

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Listar
@produto_router.get('/produto')
async def get_produto():
    return {'produto':'Acarajé'}

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Editar
@produto_router.put('/{id}')
async def editar_produto(sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        salvar_log_bd('criar','variacao','id',variacao['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return     

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Consultar Quantidade


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Desativar
@produto_router.patch('/{id}/desativar')
async def desativar_produto(sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        salvar_log_bd('criar','variacao','id',variacao['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return     

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Ativar
@produto_router.patch('/{id}/ativar')
async def ativar_produto(sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        salvar_log_bd('criar','variacao','id',variacao['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return     