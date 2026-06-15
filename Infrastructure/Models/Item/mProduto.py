from Models.base import Base, Column, Integer, String, Bool, relationship, Float

class Produto(Base):
    __tablename__ = 'produtos'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    nome = Column('Nome', String, nullable=False)
    variacoes = relationship('Variacao')
    ativo = Column('Ativo', Bool, default=True)

    def __init__(self, nome):
        self.nome = nome