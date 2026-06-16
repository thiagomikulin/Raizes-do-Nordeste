from API.Schemas.Pedido.sPedido import CriacaoSchema

from Domain.exceptions import SchemaExcept

def verificar_pedido_schema_criar(schema: CriacaoSchema):
    if not schema.filial or not schema.tipoPedido or not schema.canalPedido or not schema.forma_pagamento:
        raise SchemaExcept
