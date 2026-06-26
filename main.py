from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

from time import sleep

from Infrastructure.Models.Persona.mUsuario import Usuario

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
SECRET_KEY_REFRESH = os.getenv("SECRET_KEY_REFRESH")
ALGORITHM = os.getenv("ALGORITHM")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_HOST = os.getenv("DB_HOST")

SECRET_DECRYPTABLE = os.getenv("SECRET_DECRYPTABLE")

ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

fernet = Fernet(SECRET_DECRYPTABLE)

from Infrastructure.Models.__init__ import *


app = FastAPI()


#Criação do BD
print({
    "DB_HOST": DB_HOST,
    "DB_USER": DB_USER,
    "DB_DATABASE": DB_DATABASE,
})
url = f'mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_DATABASE}'


db = create_engine(url)


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
oauth2_schema = OAuth2PasswordBearer(tokenUrl='usuarios/login-form', auto_error=False)

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#Empresa
from API.Routes.Empresa.filial_router import filial_router
from API.Routes.Empresa.campanha_router import campanha_router
from API.Routes.Empresa.estoque_router import estoque_router
from API.Routes.Empresa.movimentos_router import movimentos_router

#Itens
from API.Routes.Itens.produto_router import produto_router
from API.Routes.Itens.ingrediente_router import ingrediente_router
from API.Routes.Itens.variacao_router import variacao_router

#Log
from API.Routes.Log.log_router import log_router

#Pedido
from API.Routes.Pedido.pedido_router import pedido_router

#Persona
from API.Routes.Persona.usuario_router import usuario_router
from API.Routes.Persona.cliente_router import cliente_router

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#Empresa
app.include_router(filial_router)
app.include_router(estoque_router)
app.include_router(campanha_router)
app.include_router(movimentos_router)

#Itens
app.include_router(ingrediente_router)
app.include_router(produto_router)
app.include_router(variacao_router)

#Pedido
app.include_router(pedido_router)

#Log
app.include_router(log_router)

#Persona
app.include_router(usuario_router)
app.include_router(cliente_router)





# https://fastapi.tiangolo.com/advanced/events/