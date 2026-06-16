from API.Schemas.Pedido.sPedido import CriacaoSchema

from Domain.exceptions import SchemaExcept, MandatoryForFillingExcept

def verificar_pedido_schema_criar(schema: CriacaoSchema):
    if not schema.filial or not schema.tipoPedido or not schema.canalPedido or not schema.forma_pagamento:
        raise SchemaExcept

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