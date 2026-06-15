from Infrastructure.Models.base import Base, Column, Integer, Boolean, ForeignKey, relationship

class Estoque(Base):
    __tablename__ = 'estoques'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    filial = Column('Filial', ForeignKey('filiais.ID'))
    itens = relationship('EstoqueItens')
    ativo = Column('Ativo', Boolean, default=True, nullable=False)

    def __init__(self, filial):
        self.filial = filial
