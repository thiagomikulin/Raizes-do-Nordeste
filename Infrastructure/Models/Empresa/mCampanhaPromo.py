from Models.base import Base, Column, Integer, String, DateTime, Bool, relationship

class CampanhaPromo(Base):
    __tablename__ = 'campanhaPromos'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    nome=Column('Nome', String(80), nullable=False)
    desconto = Column('Desconto(%)',Integer, default=0, nullable=False) 
    validade = Column('Validade', DateTime, nullable=False)
    ativo = Column('Ativo', Bool, default=False, nullable=False)
    filiais = relationship('PromoFilial', cascade="all, delete-orphan")

    def __init__(self, nome, desconto, validade):
        self.nome = nome 
        self.desconto = desconto
        self.validade = validade 