from Infrastructure.Repositories.base import Session

from API.Schemas.Pedido.sPedido import CriacaoSchema, EdicaoSchema

from Infrastructure.Models.Vendas.mPedido import Pedido

from Infrastructure.Repositories.Vendas.rePedido import status_pedido_db

from Domain.exceptions import SchemaInvalido, CamposObrigatorios, PermissionExcept, SemPermissao

def verificar_pedido_schema_criar(schema: CriacaoSchema):
    if not schema.filial or not schema.tipoPedido or not schema.canalPedido or not schema.forma_pagamento:
        raise SchemaInvalido(schema)
    
def verificar_pedido_schema_editar(schema: EdicaoSchema):
    if not schema.tipoPedido or not schema.cliente or not schema.forma_pagamento:
        raise SchemaInvalido

def verificar_tipo_pedido(schema: CriacaoSchema):
    if schema.tipoPedido == 'Entrega' and (not schema.endereco and not schema.cliente):
        raise MandatoryForFillingExcept({schema.tipoPedido:['endereco','cliente']})
    elif schema.tipoPedido == 'Mesa' and not schema.mesa:
        raise MandatoryForFillingExcept({schema.tipoPedido:['mesa']})
    elif schema.tipoPedido == 'Retirada' and not schema.chamada:
        raise MandatoryForFillingExcept({schema.tipoPedido:['chamada']})
    elif schema.tipoPedido == 'Balcão' and (not schema.chamada and not schema.cliente):
        raise MandatoryForFillingExcept({schema.tipoPedido:['chamada','cliente']})
    else:
        return
    
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
    
def progredir_status(pedido:Pedido, sessao: Session):
    match pedido.status:
        case 'Aberto':
            if len(pedido.itens) > 1:
                status = 'Fechado'
            else:
                raise PermissionExcept #Criar nova exception (não é possível fechar pedido sem itens)
        case 'Fechado':
            status = 'Preparação'
        case 'Preparação':
            status="Aguardando Coleta"
        case "Aguardando Coleta":
            if pedido.tipo == 'Entrega':
                status == "Em Trânsito"
            else:
                status="Recebido"
        case "Em Trânsito":
            status="Recebido"
    return status_pedido_db(pedido, status, sessao)
