from Models.base import Base, Column, ForeignKey, Integer, String, relationship, Bool

class Variacao(Base):
    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    nome = Column('Nome', String(80), nullable=False)
    filiais = relationship('VariacaoFilial')
    ingredientes = relationship('ItemReceita')
    ativo = Column('Ativo', Bool, default=True)

    def __init__(self, nome):
        self.nome = nome