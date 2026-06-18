from API.Routes.base import *

movimentos_router = APIRouter(prefix='/movimentos', tags=['movimento'])

# Criar entrada
@movimentos_router.post('/criar')
async def criar_movimento(schema: CriacaoSchema, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        validar_schema_movimento_criacao(schema)
        verificar_permissao(ator, 'movimento', 'criar', schema.tipo_mov)
        verificar_movimento_criacao(schema.chave_nota, sessao)
        movimento = criar_movimento_bd(schema, sessao)
        salvar_log_bd('criar','movimento','id',movimento['movimento']['id'], ator, sessao)
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
    status: str | None=None,
    filial: int | None=None,
    tipo_mov: int | None=None,
    validade: date | None=None,
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
async def editar_movimento(id, schema: EdicaoSchema, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    pass

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Confirmar movimento
@movimentos_router.patch('/{id}/confirmar')
async def confirmar_movimento():
    pass

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Itens - Consultar
@movimentos_router.get('/{id}/itens')
async def listar_movimento_itens():
    pass

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Itens - Adicionar
@movimentos_router.post('/{id}/itens/adicionar')
async def adicionar_movimento_item():
    pass
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Itens - Editar
@movimentos_router.put('/{id}/itens/{id_item}')
async def editar_movimento_item():
    pass

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Itens - Excluir



