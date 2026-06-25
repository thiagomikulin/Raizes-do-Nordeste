from Application.base import verificar_permissao
from Application.Empresa.fEstoque import consultar_quantidade_estoque
from Infrastructure.Repositories.base import Session

from API.Schemas.Pedido.sPedido import CriacaoSchema, EdicaoSchema

from Infrastructure.Models.Vendas.mPedido import Pedido, StatusCode

from Infrastructure.Repositories.Vendas.rePedido import status_pedido_db

from Domain.__exceptions__ import ItensInsuficientes, SchemaInvalido, CamposObrigatorios, PermissionExcept, SemPermissao

#Complementares
from Infrastructure.Models.Empresa.mFilial import Filial
from Infrastructure.Integracoes.mock import mock_consultar_pagamento, mock_solicitar_pagamento
    
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

    print(pedido)
    match pedido.status:
        #Se o pedido estiver atualmente como aberto
        #Validações: mais de 1 item; estoque dos itens suficiente
        case 'Aberto':
            if len(pedido.itens) == 0:
                raise ItensInsuficientes #Criar nova exception (não é possível fechar pedido sem itens)
            elif consultar_quantidade_estoque(pedido, sessao):
                pass

            else:
                status = 'Fechado'
                id_pag = mock_solicitar_pagamento(pedido.filial.conta_banc, pedido.cliente.cpf, pedido.total)
                pedido.id_pagamento = id_pag
                status_pedido_db(pedido, status, sessao)
                
        case 'Fechado':
            mock_consultar_pagamento(pedido.id_pagamento)
            status = 'Preparação'
        case 'Preparação':
            status="Aguardando Coleta"
        case "Aguardando Coleta":
            if pedido.tipo == 'Entrega':
                status = "Em Trânsito"
            else:
                status="Recebido"
        case "Em Trânsito":
            status="Recebido"
    return status_pedido_db(pedido, status, sessao)

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# def cancelar_pedido(id, ator, sessao:Session):
#     verificar_permissao(ator, 'cancelar', 'Pedido')
#     pedido = buscar_pedido()
#     verificar_dono_pedido(ator, pedido)
#     if pedido.status in [
#         StatusCode.PREPARACAO, 
#         StatusCode.AGUARDACOLETA, 
#         StatusCode.TRANSITO,
#         StatusCode.CANCELADO,
#         StatusCode.RECEBIDO,
#         StatusCode.ESTORNADO]:
#             raise 
#     else:
#         pedido_cancelado = 
    