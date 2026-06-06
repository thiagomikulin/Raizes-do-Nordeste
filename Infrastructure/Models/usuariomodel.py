from base import Base, Column, String, Integer, Boolean

class Usuario(Base):
    __tablename___ = 'usuarios'

    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    nome = Column('Nome', String, nullable=False)
    email = Column('Email', String, nullable=False)
    senha = Column('Senha', String, nullable=False)
    ativo = Column('Ativo', Boolean, default='True', nullable=False)
    cargo = Column('Cargo', String, default='Não Categorizado', nullable=False)
    #filiais

    def __init__(self, nome, email, senha, ativo=True, cargo='Não Categorizado'):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.cargo = cargo
        
