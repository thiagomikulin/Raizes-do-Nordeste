from Infrastructure.Models.base import Base, Column, Integer, String, Boolean, EnumPy, AlEnum, relationship,  ForeignKey, LargeBinary

from Infrastructure.Models.Empresa.mCampanhaPromo import CampanhaPromo

class Estrutura(str, EnumPy):
    COMPLETA = 'Completa'
    REDUZIDA = 'Reduzida'

class Filial(Base):
    __tablename__ = 'filiais'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    cidade = Column('Cidade', String(100), nullable=False)
    estrutura = Column(
        'Estrutura',
        AlEnum(
            Estrutura,
            values_callable=lambda enum: [e.value for e in enum]
        ),
        default=Estrutura.REDUZIDA,
        nullable=False
    )
    endereco = Column('Endereco', String(100), nullable=False)
    ativo = Column('Ativo', Boolean, default=True, nullable=False)
    estoque = relationship("Estoque")
    conta_banc = Column('ContaBanco', LargeBinary, nullable=False)
    campanha_promo = relationship('PromoFilial')

    def __init__(self, cidade, endereco, conta_banc):
        self.cidade = cidade
        self.endereco = endereco
        self.conta_banc = conta_banc #Na hora de salvar efetivamente, através da func, encripta