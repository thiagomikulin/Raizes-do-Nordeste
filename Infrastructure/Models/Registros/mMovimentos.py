from Models.base import Base, Column, Integer, DateTime, datetime, EnumPy, AlEnum, ForeignKey, relationship, String

class StatusMov(str, EnumPy):
    ENTREGA = 'Aguardando Entrega'
    REVISAO = 'Em Revisão'
    INCONSISTENTE = 'Inconsistente'
    CANCELADO = 'Cancelado'
    VALIDADO = 'Validado'

class TipoMov(str, EnumPy):
    ENTRADA = 'Entrada'
    SAIDA = 'Saída'

class Movimento(Base):
    __tablename__ = 'movimentos'

    id = Column('ID',Integer, primary_key=True, autoincrement=True)
    datahora = Column('DataHora', DateTime, nullable=False)
    status = Column(
        'Status',
        AlEnum(
            StatusMov, 
            values_callable=lambda enum: [e.value for e in enum]
        ),
        nullable=False,
        default=StatusMov.ENTREGA
    )
    filial = Column('Filial', ForeignKey('filiais.id'))
    tipoMov = Column(
        'Tipo',
        AlEnum(
            TipoMov, 
            values_callable=lambda enum: [e.value for e in enum]
        ),
        nullable=False
    )
    itens = relationship('ItensMovimento', cascade='all, delete')
    validade = Column('Validade', DateTime, nullable=False)
    chave_nota = Column('ChaveNota', String(44), nullable=True) #Se for saída, não terá nota logo na movimentação, apenas para registro dos gerentes

    def __init__(self,filial, tipo_mov, validade, chave_nota=None):
        self.datahora = datetime.datetime
        self.status = StatusMov.ENTREGA
        self.filial = filial
        self.tipoMov = tipo_mov
        #Não tem itens
        self.validade = validade
        self.chave_nota = chave_nota

