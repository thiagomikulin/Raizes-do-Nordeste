from Models.base import Base, Column, Integer, String, Bool, EnumPy, AlEnum, relationship, jwt, ALGORITHM, SECRET_KEY, ForeignKey
from Repositories.Empresa.reEstoque import criar_estoque_bd

class Estrutura(str, EnumPy):
    COMPLETA = 'Completa'
    REDUZIDA = 'Reduzida'

class Filial(Base):
    __tablename__ = 'filiais'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    cidade = Column('Cidade', String, nullable=False)
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
    estoque = Column('Estoque', ForeignKey('estoques.id'))
    conta_banc = Column('ContaBanco', String, nullable=False)
    campanha_promo = relationship('CampanhaPromo')

    def __init__(self, cidade, endereco, conta_banc, estoque=0,):
        self.cidade = cidade
        self.endereco = endereco
        self.estoque = estoque  #Primeiro cria a filia, depois cria o estoque e vincula com a filial
        dict_conta = {"conta": conta_banc}
        self.conta_banc = jwt.encode(dict_conta, SECRET_KEY, ALGORITHM)