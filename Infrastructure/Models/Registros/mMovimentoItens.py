from Models.base import Base, Column, Integer, ForeignKey, DateTime

class ItensMovimento(Base):
    __tablename__ = 'movimentoItens'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    ingrediente = Column('Ingrediente', ForeignKey('ingredientes.id'))
    movimentacao = Column('Movimento', ForeignKey('movimentos.id'))
    quantidade = Column('Quantidade', Integer, nullable=False)
    validade = Column('Validade', DateTime, nullable=False)

    def __init__(self, ingrediente, movimentacao, validade, quantidade=0):
        self.ingrediente = ingrediente
        self.movimentacao = movimentacao
        self.quantidade = quantidade
        self.validade = validade
