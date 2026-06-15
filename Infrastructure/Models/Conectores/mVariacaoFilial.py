from Infrastructure.Models.base import Base, Column, ForeignKey

class VariacaoFilial(Base):
    __tablename__ = 'variacoesFiliais'

    variacao = Column('Variacao', ForeignKey('variacoes.ID'), primary_key=True)
    filial = Column('Filial', ForeignKey('filiais.ID'), primary_key=True)

    def __init__(self, variacao, filial):
        self.variacao = variacao
        self.filial = filial