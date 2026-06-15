from Infrastructure.Models.base import Base, Column, Integer, String, Boolean, relationship

class Produto(Base):
    __tablename__ = 'produtos'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    nome = Column('Nome', String(80), nullable=False)
    variacoes = relationship('Variacao')
    ativo = Column('Ativo', Boolean, default=True)

    def __init__(self, nome):
        self.nome = nome