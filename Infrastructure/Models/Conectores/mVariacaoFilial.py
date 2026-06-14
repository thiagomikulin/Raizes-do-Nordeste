from Models.base import Base, Column, ForeignKey

class VariacaoFilial(Base):
    variacao = Column('Variacao', ForeignKey('variacoes.id'))
    filial = Column('Filial', ForeignKey('filiais.id'))

    def __init__(self, variacao, filial)
        self.variacao = variacao
        self.filial = filial