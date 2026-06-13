from Models.base import Base, Column, ForeignKey, Integer

class ItensPed(Base):
    __tablename__ = 'pedidoItens'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    id_ped = Column('Pedido', ForeignKey('pedidos.id'))
    variacao = Column('Variacao', ForeignKey('variacoes.id'))
    quantidade = Column('Quantidade', Integer, default=0, nullable=False)
    
    def __init__(self,id_ped, variacao, quantidade=0):
        self.id_ped = id_ped
        self.variacao = variacao
        self.quantidade = quantidade


