from sqlalchemy.orm import sessionmaker, Session

from Infrastructure.Models.base import db

async def criar_sessao():
    #verificação de existência de usuários
    try:
        Session = sessionmaker(bind=db)
        sessao = Session() #Criação de sessão (cursor)
        yield sessao
    finally:
        sessao.close()

def verificar_token(*args):
    pass