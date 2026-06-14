from Models.base import Base, Column, ForeignKey

class PromoFilial(Base):
    promocao = Column('CampanhaPromo', ForeignKey('campanhaspromos.id')
    filial = Column('Filial', ForeignKey('filiais.id')

    def __init__(self, promo, filial):
        self.promocao = promo
        self.filial = filial