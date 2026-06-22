from Infrastructure.Models.base import Base, Column, ForeignKey, Integer, String, relationship, Boolean, Float

class Variacao(Base):
    __tablename__ = 'variacoes'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    nome = Column('Nome', String(80), nullable=False)
    produto = Column('Produto', ForeignKey('produtos.ID'))
    filiais = relationship('VariacaoFilial')
    ingredientes = relationship('ItemReceita')
    preco_unitario = Column('PrecoUnitario', Float, default=0)
    ativo = Column('Ativo', Boolean, default=True)

    def __init__(self, nome, produto, preco_unitario):
        self.nome = nome
        self.produto = produto
        self.preco_unitario = preco_unitario