from Models.base import Base, Column, String, Integer, Boolean, EnumPy, AlEnum

class Cargo(str, EnumPy):
    NCLASSIFICADO = "Não Classificado"
    GERENTE = "Gerente"
    ATENDENTE = "Atendente"
    COZINHEIRO = "Cozinheiro"
    TI = "TI"
    CEO = "CEO"

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    nome = Column('Nome', String(50), nullable=False)
    email = Column('Email', String(50), nullable=False)
    senha = Column('Senha', String(200), nullable=False)
    ativo = Column('Ativo', Boolean, default=True, nullable=False)
    cargo = Column(
        'Cargo', 
        AlEnum(
            Cargo, 
            values_callable=lambda enum: [e.value for e in enum]
        ), 
        default=Cargo.NCLASSIFICADO, 
        nullable=False
    )
    #filiais

    def __init__(self, nome, email, senha, ativo=True, cargo=Cargo.NCLASSIFICADO):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.cargo = cargo