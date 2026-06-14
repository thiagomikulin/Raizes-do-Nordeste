from Models.base import Base, Column, Integer, ForeignKey

class EstoqueItens(Base):
    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    estoque = Column('Estoque', ForeignKey('estoques.id'))
    ingrediente = Column('Ingrediente', ForeignKey('ingredientes.id'))
    quantidade = Column('Quantidade', Integer, default=0, nullable=False)

    def __init__(self, estoque, ingrediente):
        self.estoque = estoque
        self.ingrediente = ingrediente