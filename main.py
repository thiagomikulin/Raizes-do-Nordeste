from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

from time import sleep

from Infrastructure.Models.Persona.mUsuario import Usuario

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_HOST = os.getenv("DB_HOST")

ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

from Infrastructure.Models.__init__ import *


app = FastAPI()

#Criação do BD
db = create_engine(f'mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_DATABASE}')


@app.on_event("startup")
async def startup_event():
    for tentativa in range(30):
        try:
            Base.metadata.create_all(db)
            print('Banco conectado')
            senha_root_cripto = bcrypt_context.hash('root')
            user_ceo = Usuario('root', 'root@root.com', senha_root_cripto, True, 'CEO')
            Session = sessionmaker(bind=db)
            sessao = Session() #Criação de sessão (cursor)
            tem_root = sessao.query(Usuario).filter(Usuario.email == 'root@root.com').first()
            if not tem_root:
                sessao.add(user_ceo)
                sessao.commit()
                sessao.close()
                print('Usuário root criado!')
            break
        except Exception as e:
            print(f'Tentativa {tentativa+1}:{e}')
            sleep(2)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_schema = OAuth2PasswordBearer(tokenUrl='usuarios/login-form')



from API.Routes.Pedido.pedido_router import pedido_router
from API.Routes.Itens.produto_router import produto_router
from API.Routes.Autenticacao.usuario_router import usuario_router
from API.Routes.Autenticacao.cliente_router import cliente_router
from API.Routes.Empresa.filial_router import filial_router

app.include_router(pedido_router)
app.include_router(produto_router)

#Autenticação
app.include_router(usuario_router)
app.include_router(cliente_router)

app.include_router(filial_router)

# https://fastapi.tiangolo.com/advanced/events/