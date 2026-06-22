#Base
from API.Routes.base import *
from Application.base import verificar_permissao, verificar_token
from Infrastructure.Repositories.base import Session, Depends, criar_sessao

from Application.chamada_rota import criar_entidade

#Exceptions
from Domain.__exceptions__ import ExceptionHTTP, ExceptionGenerica
#Logs
from Infrastructure.Repositories.Registros.reLogs import salvar_log_bd

#Requisitos
from API.Schemas.Empresa.sMovimentos import CriacaoSchema, EdicaoSchema, ItemCriacaoSchema
from Application.Registros.fMovimentos import validar_schema_movimento_criacao, validar_schema_movimento_edicao, exec_busca
from Infrastructure.Repositories.Registros.reMovimentos import verificar_movimento_criacao, criar_movimento_bd
from Infrastructure.Models.Registros.mMovimentos import Movimento

movimentos_router = APIRouter(prefix='/movimentos', tags=['empresa'])

# Criar entrada
@movimentos_router.post('/criar')
async def criar_movimento(schema: CriacaoSchema, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        movimento = criar_entidade(Movimento, schema, ator, sessao, campo_verificacao=["chave_nota"])
        # validar_schema_movimento_criacao(schema)
        # verificar_permissao(ator, 'movimento', 'criar', schema.tipo_mov)
        # verificar_movimento_criacao(schema.chave_nota, sessao)
        # movimento = criar_movimento_bd(schema, sessao)
        # salvar_log_bd('criar','movimento','id',movimento['movimento']['id'], ator, sessao)
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
    datahora: str | None=None,
    status: str | None=None,
    filial: int | None=None,
    tipo_mov: int | None=None,
    validade: str | None=None,
    chave_nota: str | None=None,
    sessao: Session = Depends(criar_sessao), 
    ator = Depends(verificar_token)
):
    try:
        verificar_permissao(ator, 'movimentos', 'listar', tipo_mov)
        lista = exec_busca(id, datahora, status, filial, tipo_mov, validade, chave_nota, sessao, ator)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return lista

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Editar
@movimentos_router.put('/{id}')
async def editar_movimento(id: int, schema: EdicaoSchema, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        validar_schema_movimento_edicao(schema)
        verificar_permissao(ator, 'movimento', 'editar', schema.tipoMov)
        movimento = verificar_movimento_existe(schema.chave_nota, sessao)
        verificar_movimento_atualizacao(schema, movimento)
        movimento_editado = editar_movimento_bd(schema, sessao)
        salvar_log_bd('criar','variacao','id',variacao['id'], ator, sessao)
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
@movimentos_router.get('/{id}/itens')
async def listar_movimento_itens(id: int, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        verificar_permissao(ator, 'movimentos', 'itens - consultar')
        itens = exec_busca()
        salvar_log_bd('criar','variacao','id',variacao['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return itens

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Itens - Adicionar
@movimentos_router.post('/{id}/itens/adicionar')
async def adicionar_movimento_item(schema: ItemCriacaoSchema, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        validar_schema_movimento_item_criacao(schema)
        verificar_permissao(ator, 'movimentos', 'itens - adicionar')
        verificar_movimento_item_add(schema.id, sessao)
        novo_item = adicionar_movimento_item_bd(schema, sessao)
        salvar_log_bd('criar','variacao','id',variacao['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return 
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Itens - Editar
@movimentos_router.put('/{id}/itens/{id_item}')
async def editar_movimento_item(sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        verificar_permissao(ator, 'movimentos', 'itens - editar')
        salvar_log_bd('criar','variacao','id',variacao['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return 

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Itens - Excluir
@movimentos_router.delete('/{id}/itens/{id_item}/excluir')
async def excluir_movimento_item(id: int, id_item: int, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        verificar_permissao(ator, 'movimentos', 'itens - excluir')
        salvar_log_bd('criar','variacao','id',variacao['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return 



