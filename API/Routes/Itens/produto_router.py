from API.Routes.base import APIRouter
from Application.base import verificar_permissao, verificar_token
from Infrastructure.Repositories.base import Session, Depends, criar_sessao
from Domain.__exceptions__ import ExceptionHTTP, ExceptionGenerica
from Infrastructure.Repositories.Registros.reLogs import salvar_log_bd

from Application.chamada_rota import ativar_entidade, criar_entidade, desativar_entidade, editar_entidade, visualizar_entidade

from API.Schemas.Itens.sProdutos import CriacaoSchema, EdicaoSchema
from Application.Item.fProduto import verificar_schema_criacao_produto
from Infrastructure.Models.Item.mProduto import Produto


produto_router = APIRouter(prefix='/produto', tags=['Itens - Produtos'])

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Criar
@produto_router.post('/criar')
async def criar_produto(schema: CriacaoSchema, sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        produto = criar_entidade(Produto, schema, ator, sessao, campo_verificacao=['nome'])
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return produto

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Listar
@produto_router.get('/produto')
async def get_produto(
    id: int | None=None,
    nome: int | None=None,
    ativo: int | None=None,
    sessao: Session = Depends(criar_sessao), 
):
    dict_campos = {
        'id':id,
        'nome':nome,
        'ativo':ativo
    }
    try:
        lista = visualizar_entidade(Produto, sessao, lista_campos=dict_campos)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    return lista

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Editar
@produto_router.put('/{id}/editar')
async def editar_produto(id: int, schema: EdicaoSchema, sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        produto_editado = editar_entidade(id, Produto, schema, ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return produto_editado

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Consultar Quantidade


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Desativar
@produto_router.patch('/{id}/desativar')
async def desativar_produto(id: int, sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        produto_ativo = desativar_entidade(Produto, ator, id, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return produto_ativo    

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Ativar
@produto_router.patch('/{id}/ativar')
async def ativar_produto(id: int, sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        produto_desativo = ativar_entidade(Produto, ator, id, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return produto_desativo    