from Domain.__exceptions__ import NaoEncontrado
from Infrastructure.Models.Vendas.mPedido import Pedido


def pedido_existe(id, sessao):
    sessao.query(Pedido).filter(Pedido.id==id).first()
    if not Pedido:
        raise NaoEncontrado({'id':id})