from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

from time import sleep

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

from Infrastructure.Models.__init__ import *
from Infrastructure.Models.base import db

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    for tentativa in range(30):
        try:
            Base.metadata.create_all(db)
            print('Banco conectado')
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