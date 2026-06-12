from Models.base import Base, Column, String, Integer, Float, AlEnum, EnumPy

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