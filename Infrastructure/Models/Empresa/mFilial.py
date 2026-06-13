from Models.base import Base, Column, Integer, String, Bool, EnumPy, AlEnum

class Estrutura(str, EnumPy):
    COMPLETA = 'Completa'
    REDUZIDA = 'Reduzida'

class Filial(Base):
    __tablename__ = 'filiais'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    cidade = Column('Cidade', '')
    estrutura = Column(
        'Estrutura',
        AlEnum(
            Estrutura,
            values_callable=lambda enum: [e.value for e in enum]
        ),
        default=Estrutura.REDUZIDA,
        nullable=False
    )
    endereco = Column('Endereco', String, nullable=False)
    ativo = Column('Ativo', Bool, default=True, nullable=False)
    #estoque = Relationship
    #conta_banc
    #campanha_promo