from Infrastructure.Repositories.base import Session


from Infrastructure.Models.Vendas.mPedido import Pedido

from API.Schemas.Pedido.sPedido import CriacaoSchema

from Domain.__exceptions__ import NotFoundExcept

def pedido_existe(id, sessao: Session):
    pedido = sessao.query(Pedido).filter(Pedido.id==id).first()
    if not pedido:
        raise NotFoundExcept(id)
    else:
        return pedido
    


def criar_pedido_bd(schema:CriacaoSchema, sessao:Session, ator):
    novo_pedido = Pedido(
        schema.filial, 
        schema.tipoPedido,
        schema.canalPedido,
        type(ator).__name__,
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

def status_pedido_db(pedido:Pedido, status: str, sessao: Session):
    pedido.status == status
    sessao.commit()
    return {
        "message":"Status atualizado com sucesso!",
        "pedido":{
            "id":pedido.id,
            "status":pedido.status
        }
    }
    

