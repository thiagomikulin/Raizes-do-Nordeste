from Models.base import Base, Column, String, Integer, Float, Date, ForeignKey, AlEnum, EnumPy
from Models.Persona.mCliente import Cliente
from Models.Persona.mUsuario import Usuario

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
    MOCK = "Mock",
    CREDITO = "Crédito"
    DEBITO = "Débito"

class TipoLogin(Usuario, Cliente, EnumPy):
    USUARIO = Usuario
    CLIENTE = Cliente

class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    #filial
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
    cliente = Column("Cliente", ForeignKey('clientes.id'), nullable=True)
    tipo_modificador = Column(
        'Modificador',
        AlEnum(
            TipoLogin,
            values_callable=lambda enum: [e.value for e in enum]
        ),
        nullable=False
    )
    id_modificador = Column("IdModificador", Integer, nullable=False)
    data = Column("Data", Date, nullable=False)
    mesa = Column("Mesa", Integer, nullable=False)
    #itens = Relationship()
    chamada = Column("Chamada", Integer)
    endereco = Column("Endereco", String)
    soma_itens = Column("SomaItens", Float, default=0, nullable=False)
    frete = Column("Frete", Float, default=0, nullable=False)
    total = Column("Total", Float, default=0, nullable=False)
    forma_pagamento = Column(
        "Total",
        AlEnum(
            FormaPagamento,
            values_callable=lambda enum: [e.value for e in enum]
        ), 
        default=FormaPagamento.MOCK,
        nullable=False
        )
    desconto_fidelidade = Column("PontosFidelidade", Integer, default=0, nullable=False)
