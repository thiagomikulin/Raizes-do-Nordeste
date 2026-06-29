from API.Routes.base import APIRouter
from Application.base import verificar_token, verificar_permissao
from Application.Empresa.fEstoque import consultar_quantidade_estoque, consultar_quantidade_estoque_item, consultar_quantidade_estoque_variacao
from Infrastructure.Models.Item.mVariacao import Variacao
from Infrastructure.Repositories.Vendas.rePedido import status_pedido_db
from Infrastructure.Repositories.Pedido.rePedido import pedido_existe
from Infrastructure.Repositories.base import Session, Depends, criar_sessao, verificar_entidade_existe
from Application.chamada_rota import criar_entidade, editar_entidade, excluir_entidade, visualizar_entidade


from API.Schemas.Pedido.sPedido import CriacaoSchema, EdicaoSchema
from API.Schemas.Pedido.sPedItens import InternoItemCriacaoSchema, InternoItemEdicaoSchema, ItemCriacaoSchema, ItemEdicaoSchema, ItemExclusaoSchema

from Application.Vendas.fPedido import aumentar_valor_pedido, cancelar_status, detecta_alteracao_quantidade, diminuir_valor_pedido, verificar_dono_pedido, progredir_status

from Infrastructure.Models.Vendas.mPedido import Pedido
from Infrastructure.Models.Vendas.mPedidoItens import ItensPed


from Domain.__exceptions__ import ExceptionGenerica, ExceptionHTTP

pedido_router = APIRouter(prefix='/pedidos', tags=['Pedidos'])

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Criar
@pedido_router.post('/criar', status_code=201)
async def criar_pedido(schema: CriacaoSchema, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    """
    Cria um novo pedido a partir dos dados passados
    """
    path='/pedidos/criar'
    try:
        #Pode verificar também se o usuário (se for usuário) é um trabalhador da mesma filial que o pedido. Se não for, deve impedir a criação (implementação futura)
        #Validação de mesa, cliente e entrega feita no schema
        pedido = criar_entidade(Pedido, schema, ator, sessao, campo_verificacao=None, lista_regras_validacao=None)
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
@pedido_router.patch('/{id}/status')
async def atualizar_status_pedido(id: int, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    #OBS: colocar validação extra para clientes (só atualizam status de pedido para Recebido - confirma recebimento)
    try:
        pedido = pedido_existe(id, sessao) #verifica se o pedido existe
        verificar_permissao(ator, 'atualizar campo', 'Pedido') #verifica se o ator pode criar
        verificar_dono_pedido(ator, pedido) #verifica se o ator é cliente e se for, se o pedido é dele
        pedido_update = progredir_status(pedido, sessao) #atualiza o status do pedido manualmente
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return pedido_update
    

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Cancelar
@pedido_router.patch('/{id}/status/cancelar')
async def cancelar_pedido(id: int, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        pedido = pedido_existe(id, sessao) #verifica se o pedido existe
        verificar_permissao(ator, 'atualizar campo', 'Pedido') #verifica se o ator pode criar
        verificar_dono_pedido(ator, pedido) #verifica se o ator é cliente e se for, se o pedido é dele
        pedido_cancelado = cancelar_status(pedido, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return pedido_cancelado


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Consultar
@pedido_router.get('/')
async def consultar_pedido(
    id: int | None=None,
    filial: int | None=None,
    status:str | None=None,
    tipo:str | None=None,
    canalPedido:str | None=None,
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
        "canal":canalPedido, 
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

# Itens - Adicionar
@pedido_router.post('/{id}/itens/adicionar', status_code=201)
async def adicionar_item_pedido(id: int, schema: ItemCriacaoSchema, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    schema_int = InternoItemCriacaoSchema(variacao=schema.variacao, quantidade=schema.quantidade, id_ped=id)
    try:
        #Pedido
        verificar_entidade_existe(Pedido, id, sessao)
        #Item do pedido
        verificar_entidade_existe(Variacao, schema_int.variacao, sessao)
        item_pedido = criar_entidade(ItensPed, schema_int, ator, sessao, ['id_ped', 'variacao'], lista_regras_validacao=[consultar_quantidade_estoque_variacao],lista_regras_pos=[aumentar_valor_pedido])
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    return item_pedido
    

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Itens - Remover
@pedido_router.delete('/{id_ped}/itens/{id}/remover')
async def remover_item_pedido(id_ped: int, id: int, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    schema = ItemExclusaoSchema(id_ped=id_ped, id=id)
    try:
        item_deletado = excluir_entidade(ItensPed, schema, ator, sessao, ['id', 'id_ped'], lista_regras_pos=[diminuir_valor_pedido])
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    return item_deletado

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Itens - Editar
@pedido_router.put('/{id_ped}/itens/{id}/editar')
async def editar_item_ped(schema: ItemEdicaoSchema, id_ped: int, id: int, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    dict_campos = {'id_ped':id_ped, 'id':id}
    schema_int = InternoItemEdicaoSchema(id=id, variacao=schema.variacao, quantidade=schema.quantidade)
    try:
        #Validação prévia se esse item pertence a esse pedido
        visualizar_entidade(ItensPed, sessao, ator, dict_campos)
        item_editado = editar_entidade(id, ItensPed, schema_int, ator, sessao, lista_regras_validacao=[consultar_quantidade_estoque_item],lista_regras_pos=[detecta_alteracao_quantidade])
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    return item_editado


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Itens - Consultar
@pedido_router.get('/{id}/itens/')
async def consultar_itens_pedido(id: int, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    dict_campos = {"id_ped":id}
    try:
        lista_itens = visualizar_entidade(ItensPed, sessao, ator, dict_campos)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    return lista_itens



