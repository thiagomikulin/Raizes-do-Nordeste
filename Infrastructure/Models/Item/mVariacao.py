from Models.base import Base, Column, ForeignKey, Integer, String, relationship, Bool, Float

class Variacao(Base):
    __tablename__ = 'variacoes'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    nome = Column('Nome', String(80), nullable=False)
    filiais = relationship('VariacaoFilial')
    ingredientes = relationship('ItemReceita')
    preco_unitario = Column('PrecoUnitario', Float, default=0)
    ativo = Column('Ativo', Bool, default=True)

    def __init__(self, nome, preco):
        self.nome = nome
        self.preco_unitario = preco