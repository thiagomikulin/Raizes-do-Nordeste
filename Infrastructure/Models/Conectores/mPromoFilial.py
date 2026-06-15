from Models.base import Base, Column, ForeignKey, Bool

class PromoFilial(Base):
    promocao = Column('CampanhaPromo', ForeignKey('campanhaspromos.id')
    filial = Column('Filial', ForeignKey('filiais.id')
    ativo = Column('Ativo', Bool, default=True)

    def __init__(self, promo, filial):
        self.promocao = promo
        self.filial = filial