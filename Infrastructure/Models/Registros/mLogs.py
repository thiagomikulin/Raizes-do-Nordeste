from Infrastructure.Models.base import Base, Column, Integer, String, AlEnum, EnumPy, DateTime, TipoLogin, datetime

class Tabelas(str, EnumPy):
    PEDIDO = 'pedidos'
    PEDIDOITEM = 'pedidoItens'
    MOVIMENTO = 'movimentos'
    MOVIMENTOITEM = 'movimentoItens'
    USUARIO = 'usuarios'
    CLIENTE = 'clientes'
    VARIACAO = 'variacoes'
    PRODUTO = 'produtos'
    INGREDIENTE = 'ingredientes'
    FILIAL = 'filiais'
    ESTOQUEITEM = 'estoqueItens'
    ESTOQUE = 'estoques'
    CAMPANHAPROMO = 'campanhaPromos'
    VARIACAOFILIAL = 'variacoesFiliais'
    USUARIOFILIAL = 'usuariosFiliais'
    PROMOFILIAL = 'filiaisPromos'
    ITEMRECEITA = 'receitasItens'

class Acoes(str, EnumPy):
    CRIAR = 'criar'
    ATIVAR = 'ativar'
    DESATIVAR = 'desativar'
    EDITAR = 'editar'
    EXCLUIR = 'excluir'
    ALTERAR_STATUS = 'alterar status'
    ATUALIZAR_CAMPO = 'atualizar campo'

class Log(Base):
    __tablename__ = 'logs'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    acao = Column(
        'Acao', 
        AlEnum(
            Acoes,
            values_callable=lambda enum: [e.value for e in enum]
        ), 
        nullable=False
    )
    tabela = Column(
        'Tabela',
        AlEnum(
            Tabelas,
            values_callable=lambda enum: [e.value for e in enum]
        )    
    )
    id_modificado = Column('IdModificado', String(12), nullable=False)
    campo = Column('Campo', String(100), nullable=False)
    valor_ant = Column('ValorAnterior', String(200), nullable=False)
    valor_novo = Column('ValorNovo', String(200), nullable=False)
    tipo_pessoa = Column(
        'TipoPessoa',
        AlEnum(
            TipoLogin,
            values_callable=lambda enum: [e.value for e in enum]
        )
    )
    id_pessoa = Column('IdPessoa', Integer, nullable=False)
    datahora = Column('DataHora', DateTime, nullable=False)

    def __init__(self, acao, tabela, id_modificado, campo, valor_ant, valor_novo, tipo_pessoa, id_pessoa):
        self.acao = acao
        self.tabela = tabela
        self.id_modificado = id_modificado
        self.campo = campo
        self.valor_ant = valor_ant
        self.valor_novo = valor_novo
        self.tipo_pessoa = tipo_pessoa
        self.id_pessoa = id_pessoa
        self.datahora = datetime.datetime.now()
