from Models.base import Base, Column, Integer, Bool, ForeignKey, relationship

class Estoque(Base):
    __tablename__ = 'estoques'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    filial = Column('Filial', ForeignKey('filiais.id'))
    itens = relationship('EstoqueItens')
    ativo = Column('Ativo', Bool, default=True, nullable=False)

    def __init__(self, filial):
        self.filial = filial
