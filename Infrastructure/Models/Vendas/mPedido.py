from Infrastructure.Models.base import Base, Column, String, Integer, Float, DateTime, ForeignKey, AlEnum, EnumPy, TipoLogin, datetime, relationship

class StatusCode(str, EnumPy):
    ABERTO = "Aberto"
    FECHADO = "Fechado"
    PREPARACAO = "Preparação"
    AGUARDACOLETA = "Aguardando Coleta"
    TRANSITO = "Em Trânsito"
    CANCELADO = "Cancelado"
    RECEBIDO = "Recebido"
    ESTORNADO = "Estornado"

class TiposPed(str, EnumPy):
    ENTREGA = "Entrega"
    MESA = "Mesa"
    RETIRADA = "Retirada"
    BALCAO = "Balcão"

class CanalPedido(str, EnumPy):
    APP = "App"
    TOTEM = "Totem"
    RETIRADA = "Retirada"
    PICKUP = "Pickup"
    WEB = "Web"

class FormaPagamento(str, EnumPy):
    MOCK = "Mock"
    CREDITO = "Crédito"
    DEBITO = "Débito"

class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    filial = Column('Filial', ForeignKey('filiais.ID'))
    status = Column(
        'Status', 
        AlEnum(
            StatusCode, 
            values_callable=lambda enum: [e.value for e in enum]
        ),
        default=StatusCode.ABERTO, 
        nullable=False
    )
    tipo = Column(
        'Tipo',
        AlEnum(
            TiposPed,
            values_callable=lambda enum: [e.value for e in enum]
        ),
        default=TiposPed.BALCAO,
        nullable=False
    )
    canal = Column(
        'Canal',
        AlEnum(
            CanalPedido,
            values_callable=lambda enum: [e.value for e in enum]
        ),
        default=CanalPedido.RETIRADA,
        nullable=False
    )
    tipo_criador = Column(
        'Criador',
        AlEnum(
            TipoLogin,
            values_callable=lambda enum: [e.value for e in enum]
        ),
        nullable=False
    )
    id_criador = Column("IdCriador", Integer, nullable=False)
    cliente = Column("Cliente", ForeignKey('clientes.ID'), nullable=True)
    tipo_modificador = Column(
        'Modificador',
        AlEnum(
            TipoLogin,
            values_callable=lambda enum: [e.value for e in enum]
        ),
        nullable=False
    )
    id_modificador = Column("IdModificador", Integer, nullable=False)
    datahora = Column("DataHora", DateTime, nullable=False)
    mesa = Column("Mesa", Integer, nullable=True)
    itens = relationship('ItensPed', cascade='all, delete')
    chamada = Column("Chamada", Integer)
    endereco = Column("Endereco", String(80))
    soma_itens = Column("SomaItens", Float, default=0, nullable=False)
    frete = Column("Frete", Float, default=0, nullable=False)
    total = Column("Total", Float, default=0, nullable=False)
    forma_pagamento = Column(
        "FormaPagamento",
        AlEnum(
            FormaPagamento,
            values_callable=lambda enum: [e.value for e in enum]
        ), 
        default=FormaPagamento.MOCK,
        nullable=False
        )
    id_pagamento = Column("IdPagamento", Integer)
    status_pagamento = Column("StatusPagamento", String(80))
    desconto_fidelidade = Column("PontosFidelidade", Integer, default=0, nullable=False)

    def __init__(self, filial, tipo_ped, canal, tipo_criador, id_criador, cliente=None, mesa=None, chamada=None, endereco = None, forma_pagamento=None):
        self.filial = filial
        self.status = StatusCode.ABERTO
        self.tipo = tipo_ped
        self.canal = canal
        self.tipo_criador = tipo_criador
        self.id_criador = id_criador
        self.cliente = cliente
        self.tipo_modificador = tipo_criador #Incialmente, e apenas na criação
        self.id_modificador = id_criador
        self.datahora = datetime.datetime.now()
        self.mesa = mesa
        self.chamada = chamada
        self.endereco = endereco
        self.forma_pagamento = forma_pagamento
        