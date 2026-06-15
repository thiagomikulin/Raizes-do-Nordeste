from Models.base import Base, Column, ForeignKey, Float, String

class ItemReceita(Base):
    variacao = Column('Variacao',ForeignKey('variacoes.id'))
    ingrediente = Column('Ingredientes', ForeignKey('ingredientes.id'))
    quantidade = Column('Quantidade', Float, default=0, nullable=False)
    unidade_medida = Column('UnidadeMedida', String(2), default='UN', nullable=False)

    def __init__(self, variacao, ingrediente, quantidade, unidade_medida=0):
        self.variacao = variacao
        self.ingrediente = ingrediente
        self.quantidade = quantidade 
        self.unidade_medida = unidade_medida