from Infrastructure.Models.Vendas.mPedidoItens import ItensPed
from Infrastructure.Repositories.Persona.reCliente import verificar_cliente_existe
from Infrastructure.Repositories.Empresa.reFilial import verificar_filial_existe
from main import fernet
from Application.base import verificar_permissao
from Application.Empresa.fEstoque import consultar_quantidade_estoque
from Infrastructure.Repositories.base import Session

from API.Schemas.Pedido.sPedido import CriacaoSchema, EdicaoSchema

from Infrastructure.Models.Vendas.mPedido import Pedido, StatusCode, StatusPagamento

from Infrastructure.Repositories.Vendas.rePedido import aumentar_valor_pedido_db, diminuir_valor_pedido_db, pedido_existe, status_pedido_db

from Domain.__exceptions__ import AlteraPedidoNaoPermitido, ItensInsuficientes, SchemaInvalido, CamposObrigatorios, PermissionExcept, SemPermissao

#Complementares
from Infrastructure.Models.Empresa.mFilial import Filial
from Infrastructure.Integracoes.mock import mock_cancelar_pagamento, mock_consultar_pagamento, mock_solicitar_pagamento
    
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def verificar_dono_pedido(ator, pedido:Pedido):
    if type(ator).__name__ == 'Cliente':
        if ator.id != pedido.cliente:
            raise SemPermissao(ator)
        else:
            if pedido.status != 'Aberto':
                raise SemPermissao(ator)
            return True
        
    else:
        return True
    
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def progredir_status(pedido:Pedido, sessao: Session):

    match pedido.status:
        #Se o pedido estiver atualmente como aberto
        #Validações: mais de 1 item; estoque dos itens suficiente
        case 'Aberto':
            if len(pedido.itens) == 0:
                raise ItensInsuficientes #Criar nova exception (não é possível fechar pedido sem itens)
            else:
                consultar_quantidade_estoque(pedido, sessao)
                filial = verificar_filial_existe(pedido.filial, sessao)
                cliente = verificar_cliente_existe(sessao, id=pedido.cliente)
                conta_banc = str(fernet.decrypt(filial.conta_banc))
                print(conta_banc)
                pagamento = mock_solicitar_pagamento(conta_banc, cliente.cpf, pedido.total)
                pedido.id_pagamento = pagamento['pagamento']['id']
                if pagamento['pagamento']['status'] == 'Solicitado':
                    status_pag = StatusPagamento.PENDENTE
                else:
                    status_pag = StatusPagamento.AGUARDANDO
                pedido.status_pagamento = status_pag
                novo_status = 'Fechado'
        case 'Fechado':
            resultado_pagamento = mock_consultar_pagamento(pedido.id_pagamento)
            if resultado_pagamento['status'] == 'Cancelado':
                pedido.status_pagamento = resultado_pagamento['status']
                novo_status = 'Cancelado'
            elif resultado_pagamento['status'] == 'Estornado':
                pedido.status_pagamento = resultado_pagamento['status']
                novo_status = 'Estornado'
            elif resultado_pagamento['status'] == 'Aprovado':
                pedido.status_pagamento = resultado_pagamento['status']
                novo_status = 'Preparação'
        case 'Preparação':
            novo_status="Aguardando Coleta"
        case "Aguardando Coleta":
            if pedido.tipo == 'Entrega':
                novo_status = "Em Trânsito"
            else:
                novo_status="Recebido"
        case "Em Trânsito":
            novo_status="Recebido"
        case "Cancelado":
            raise AlteraPedidoNaoPermitido(pedido.status)
        case 'Estornado':
            raise AlteraPedidoNaoPermitido(pedido.status)
    return status_pedido_db(pedido, novo_status, sessao)

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def cancelar_status(pedido: Pedido, sessao:Session):
    pag_cancelado = mock_cancelar_pagamento(pedido.id_pagamento)
    if pag_cancelado.status_code != 200:
        raise
    else:
        pedido_cancelado = status_pedido_db(pedido, 'Cancelado', sessao)
        return pedido_cancelado
    
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    
def aumentar_valor_pedido(item_ped: ItensPed, sessao: Session):
    pedido = pedido_existe(item_ped.id_ped, sessao)
    aumentar_valor_pedido_db(item_ped, pedido, sessao)

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def diminuir_valor_pedido(item_ped: ItensPed, sessao: Session):
    pedido = pedido_existe(item_ped.id_ped, sessao)
    diminuir_valor_pedido_db(item_ped, pedido, sessao)