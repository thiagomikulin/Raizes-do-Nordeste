from Infrastructure.Repositories.base import Session

from Infrastructure.Models.Persona.mCliente import Cliente
from Infrastructure.Models.Vendas.mPedido import Pedido

from API.Schemas.Pedido.sPedido import CriacaoSchema

from Domain.exceptions import NotFoundExcept

def cliente_existe(id, sessao: Session):
    cliente = sessao.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        raise NotFoundExcept

def criar_pedido_bd(schema:CriacaoSchema, sessao:Session, ator):
    novo_pedido = Pedido(
        schema.filial, 
        'Aberto',
        schema.canalPedido,
        str(type(ator)),
        ator.id,
        schema.cliente,
        schema.mesa,
        schema.chamada,
        schema.endereco,
        schema.forma_pagamento
        )
    sessao.add(novo_pedido)
    sessao.commit()
    return {
        "message":"pedido criado com sucesso!",
        "pedido":{
            "id":novo_pedido.id,
            "filial":novo_pedido.filial,
            "status":novo_pedido.status,
            "tipo":novo_pedido.tipo,
            "canal":novo_pedido.canal,
            "cliente":novo_pedido.cliente,
            "datahora":novo_pedido.datahora,
            "mesa":novo_pedido.mesa,
            "chamada":novo_pedido.chamada,
            "endereco":novo_pedido.endereco,
            "formaPagamento":novo_pedido.forma_pagamento
        }
    }