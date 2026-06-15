from Models.base import Base, Column, ForeignKey, Bool

class PromoFilial(Base):
    __tablename__ = 'filiaisPromos'

    promocao = Column('CampanhaPromo', ForeignKey('campanhaspromos.id'), primary_key=True)
    filial = Column('Filial', ForeignKey('filiais.id'), primary_key=True)
    ativo = Column('Ativo', Bool, default=True)

    def __init__(self, promo, filial):
        self.promocao = promo
        self.filial = filial