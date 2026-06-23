from API.Routes.base import APIRouter
from Application.base import verificar_token, verificar_permissao
from Infrastructure.Repositories.base import Session, Depends, criar_sessao


from Application.chamada_rota import criar_entidade, editar_entidade, visualizar_entidade

from API.Schemas.Pedido.sPedido import *

from Application.Vendas.fPedido import verificar_pedido_schema_criar,verificar_pedido_schema_editar , verificar_tipo_pedido, verificar_dono_pedido, progredir_status
from Infrastructure.Models.Vendas.mPedido import Pedido


from Infrastructure.Repositories.Vendas.rePedido import criar_pedido_bd, pedido_existe
from Infrastructure.Repositories.Persona.reCliente import cliente_existe
from Infrastructure.Repositories.Registros.reLogs import salvar_log_bd

from Domain.__exceptions__ import ExceptionGenerica, ExceptionHTTP

pedido_router = APIRouter(prefix='/pedidos', tags=['Pedido'])

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Criar
@pedido_router.post('/criar')
async def criar_pedido(schema: CriacaoSchema, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    """
    Cria um novo pedido a partir dos dados passados
    """
    path='/pedidos/criar'
    try:
        #Pode verificar também se o usuário (se for usuário) é um trabalhador da mesma filial que o pedido. Se não for, deve impedir a criação (implementação futura)
        #Validação de mesa, cliente e entrega feita no schema
        pedido = criar_entidade(Pedido, schema, ator, sessao, campo_verificacao=None, lista_regras_validacao=None)
        # verificar_pedido_schema_criar(schema)
        # verificar_permissao(ator, 'pedido', 'criar')
        # verificar_tipo_pedido(schema) #consistência de mesas, clientes e entregas
        # cliente_existe(schema.cliente, sessao)
        # pedido = criar_pedido_bd(schema, sessao, ator)
        # salvar_log_bd('criar','pedidos','id',pedido['pedido']['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return pedido

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Editar
@pedido_router.put('/{id}/editar')
async def editar_pedido(id:int, schema: EdicaoSchema, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):

    #OBS: colocar validação extra para clientes (só atualizam pedidos com status=aberto)
    try:
        pedido_editado = editar_entidade(id, Pedido, schema, ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    return pedido_editado

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# AtualizarStatus
@pedido_router.patch('/status/{id}')
async def atualizar_status_pedido(id: int, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    path = f'/pedidos/status/{id}'

    #OBS: colocar validação extra para clientes (só atualizam status de pedido para Recebido - confirma recebimento)
    try:
        pedido = pedido_existe(id, sessao) #verifica se o pedido existe
        verificar_permissao(ator, 'pedido', 'atualizar_status') #verifica se o ator pode criar
        verificar_dono_pedido(ator, pedido) #verifica se o ator é cliente e se for, se o pedido é dele
        pedido_update = progredir_status(pedido, sessao) #atualiza o status do pedido manualmente
    except NotFoundExcept as e:
        raise NaoEncontrado(path, e.campos)
    else:
        return pedido_update
    



#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Consultar
@pedido_router.get('/')
async def consultar_pedido(
    id: int | None=None,
    filial: int | None=None,
    status:str | None=None,
    tipo:str | None=None,
    canal:str | None=None,
    tipo_criador:str | None=None,
    id_criador:int | None=None,
    cliente:int | None=None,
    tipo_modificador:str | None=None,
    id_modificador:int | None=None,
    forma_pagamento:str | None=None,
    sessao: Session = Depends(criar_sessao), 
    ator=Depends(verificar_token)
):
    dict_campos = {
        "id":id, 
        "filial":filial, 
        "status":status, 
        "tipo":tipo, 
        "canal":canal, 
        "tipo_criador":tipo_criador, 
        "id_criador":id_criador, 
        "cliente":cliente, 
        "tipo_modificador":tipo_modificador, 
        "id_modificador":id_modificador, 
        "forma_pagamento":forma_pagamento, 
    }
    try:
        lista = visualizar_entidade(Pedido, sessao, ator, lista_campos=dict_campos)
        # verificar_permissao(ator, 'pedido', 'consultar')
        # lista = exec_busca(, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return lista

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Cancelar

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Itens - Adicionar

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Itens - Remover

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Itens - Editar

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Itens - Consultar



