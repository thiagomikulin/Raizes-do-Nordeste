#Base
from datetime import date

from API.Routes.base import *
from Application.base import verificar_permissao, verificar_token
from Infrastructure.Models.Registros.mMovimentoItens import ItensMovimento
from Infrastructure.Repositories.base import Session, Depends, criar_sessao

from Application.chamada_rota import criar_entidade, editar_entidade, excluir_entidade, visualizar_entidade

#Exceptions
from Domain.__exceptions__ import ExceptionHTTP, ExceptionGenerica
#Logs
from Infrastructure.Repositories.Registros.reLogs import salvar_log_bd

#Requisitos
from API.Schemas.Empresa.sMovimentos import CriacaoSchema, EdicaoSchema, InternoItemCriacaoSchema, ItemCriacaoSchema, ItemEdicaoSchema, ItemExclusaoSchema
from Application.Registros.fMovimentos import validar_schema_movimento_criacao, validar_schema_movimento_edicao, exec_busca
from Infrastructure.Repositories.Registros.reMovimentos import verificar_movimento_criacao, criar_movimento_bd
from Infrastructure.Models.Registros.mMovimentos import Movimento, StatusMov, TipoMov

movimentos_router = APIRouter(prefix='/movimentos', tags=['Empresa - Movimentos'])

# Criar entrada
@movimentos_router.post('/criar')
async def criar_movimento(schema: CriacaoSchema, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        movimento = criar_entidade(Movimento, schema, ator, sessao, campo_verificacao=["chave_nota"])
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return movimento


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Visualizar
@movimentos_router.get('/')
async def listar_movimentos(
    id: int | None=None,
    datahora: date | None=None,
    status: StatusMov | None=None,
    filial: int | None=None,
    tipo_mov: TipoMov | None=None,
    validade: str | None=None,
    chave_nota: str | None=None,
    sessao: Session = Depends(criar_sessao), 
    ator = Depends(verificar_token)
):
    dict_campos = {
        'id':id,
        'datahora':datahora,
        'status':status,
        'filial':filial,
        'tipo_mov':tipo_mov,
        'validade':validade,
        'chave_nota':chave_nota
    }
    try:
        lista = visualizar_entidade(Movimento, sessao, ator, dict_campos)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return lista

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Editar
@movimentos_router.put('/{id}/editar')
async def editar_movimento(id: int, schema: EdicaoSchema, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        movimento_editado = editar_entidade(id, Movimento, schema, ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return movimento_editado

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Avançar movimento
@movimentos_router.patch('/{id}/status')
async def avancar_movimento(id: int, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        verificar_permissao(ator, 'movimento', 'avançar')
        movimento = verificar_movimento_existe(id, sessao)
        mov_atualizado = avancar_movimento_bd(movimento, sessao)
        salvar_log_bd('criar','variacao','id',variacao['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return mov_atualizado

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Itens - Consultar
@movimentos_router.get('/{movimentacao}/itens/')
async def listar_movimento_itens(
    id: int | None=None, 
    ingrediente: int | None=None,
    movimentacao: int | None=None,
    validade: date | None=None,
    sessao:Session = Depends(criar_sessao), 
    ator=Depends(verificar_token)):
    dict_campos = {
        "id":id,
        "ingrediente":ingrediente,
        "movimentacao":movimentacao,
        "validade":validade
    }

    try:
        itens = visualizar_entidade(ItensMovimento, sessao, ator, dict_campos)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return itens

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Itens - Adicionar
@movimentos_router.post('/{id}/itens/adicionar')
async def adicionar_movimento_item(id: int, schema: ItemCriacaoSchema, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    schema_interno = InternoItemCriacaoSchema(
        movimentacao=id, 
        ingrediente = schema.ingrediente,
        quantidade = schema.quantidade,
        validade = schema.validade
    )
    try:
        item_movimento_novo = criar_entidade(ItensMovimento, schema_interno, ator, sessao, ['ingrediente', 'movimentacao'])
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return item_movimento_novo
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Itens - Editar
@movimentos_router.put('/{id}/itens/{id_item}')
async def editar_movimento_item(schema: ItemEdicaoSchema, id: int, id_item: int, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    dict_campos = {'movimentacao':id, 'id':id_item}
    try:
        visualizar_entidade(ItensMovimento, sessao, ator, dict_campos)
        item_movimento_editado = editar_entidade(id, ItensMovimento, schema, ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return item_movimento_editado

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Itens - Excluir
@movimentos_router.delete('/{id}/itens/{id_item}/excluir')
async def excluir_movimento_item(id: int, id_item: int, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    schema = ItemExclusaoSchema(movimentacao=id, id=id_item)
    try:
        item_movimento_excluido = excluir_entidade(ItensMovimento, schema, ator, sessao, ['id', 'movimentacao'])
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return item_movimento_excluido



