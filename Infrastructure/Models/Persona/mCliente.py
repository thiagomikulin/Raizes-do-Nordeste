from Models.base import Base, Column, String, Integer, Boolean, Date

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    nome = Column('Nome', String(50), nullable=False)
    email = Column('Email', String(50), nullable=False)
    cpf = Column('CPF', String(50), nullable = False)
    scanFace = Column('Escaneamento_facial', String(200))
    senha = Column('Senha', String(200), nullable=False)
    endereco = Column('Endereço', String(80), nullable=True)
    fidelidade = Column('Fidelidade', Integer, nullable=False)
    data_nasc = Column('Nascimento', Date, nullable=False)
    ativo = Column('Ativo', Boolean, default=True, nullable=False)

    def __init__(self, nome, email, cpf, scanFace, senha, endereco, fidelidade, data_nasc, ativo=True, ):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.scanFace = scanFace
        self.senha = senha
        self.endereco = endereco
        self.fidelidade = fidelidade
        self.data_nasc = data_nasc
        self.ativo = ativo