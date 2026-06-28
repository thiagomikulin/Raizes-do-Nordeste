#Bases
from API.Routes.base import *
from Application.chamada_rota import criar_entidade, editar_entidade, visualizar_entidade
from Application.Empresa.fEstoque import consultar_quantidade_estoque, consultar_quantidade_estoque_individual
from Infrastructure.Repositories.base import Session, Depends, criar_sessao
from Application.base import verificar_token

#Exceptions
from Domain.__exceptions__ import ExceptionGenerica, ExceptionHTTP

#Requisitos
from API.Schemas.Empresa.sEstoque import InternoItemCriacaoSchema, ItemCriacaoSchema, ItemEdicaoSchema
from Infrastructure.Models.Empresa.mEstoqueItens import EstoqueItens
from Infrastructure.Models.Empresa.mEstoque import Estoque


estoque_router = APIRouter(prefix='/estoques', tags=['Empresa - Estoques']) 

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
    dict_campos = {
        "id":id,
        'filial':filial,
        'ativo':ativo
    }
    try:
        lista = visualizar_entidade(Estoque, sessao, ator, dict_campos)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return lista

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

@estoque_router.get('/itens/quantidade/')
async def exibir_quantidades(id_variacao: int, id_estoque: int, sessao:Session = Depends(criar_sessao)):
    try:
        consultado = consultar_quantidade_estoque_individual(id_variacao, id_estoque, sessao)
    except Exception as e:
        raise ExceptionGenerica(e)
    return consultado

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Itens - Criar (EstoqueItens)
@estoque_router.post('/{id}/itens/criar', status_code=201)
async def criar_estoque_itens(id_estoque: int, schema: ItemCriacaoSchema, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    schema_interno = InternoItemCriacaoSchema(estoque=id_estoque, ingrediente=schema.ingrediente, unidade_medida=schema.unidade_medida)
    try:
        item_novo = criar_entidade(EstoqueItens, schema_interno, ator, sessao, ['estoque', 'ingrediente'])
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return item_novo

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Itens - Editar (EstoqueItens)
@estoque_router.put('/itens/{id}/editar')
async def editar_estoque_itens(id: int, schema:ItemEdicaoSchema, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        item_editado = editar_entidade(id, EstoqueItens, schema, ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return item_editado

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-