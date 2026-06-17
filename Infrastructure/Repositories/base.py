

from main import db, sessionmaker, Session

from Application.base import *

async def criar_sessao():
    #verificação de existência de usuários
    try:
        Session = sessionmaker(bind=db)
        sessao = Session() #Criação de sessão (cursor)
        yield sessao
    finally:
        sessao.close()
