from Models.base import Base, Column, Integer, Bool, ForeignKey

class Estoque(Base):
    __tablename__ = 'estoques'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    filial = Column('Filial', ForeignKey('filiais.id'))
    #itens
    ativo = Column('Ativo', Bool, default=True, nullable=False)