from Infrastructure.Models.base import Base, Column, ForeignKey, Boolean

class PromoFilial(Base):
    __tablename__ = 'filiaisPromos'

    promocao = Column('CampanhaPromo', ForeignKey('campanhaPromos.ID'), primary_key=True)
    filial = Column('Filial', ForeignKey('filiais.ID'), primary_key=True)
    ativo = Column('Ativo', Boolean, default=True)

    def __init__(self, promocao, filial):
        self.promocao = promocao
        self.filial = filial