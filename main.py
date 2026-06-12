from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_schema = OAuth2PasswordBearer(tokenUrl='usuarios/login-form')

from API.Routes.Pedido.pedido_router import pedido_router
from API.Routes.Itens.produto_router import produto_router
from API.Routes.Autenticacao.usuario_router import usuario_router
from API.Routes.Autenticacao.cliente_router import cliente_router

app.include_router(pedido_router)
app.include_router(produto_router)

#Autenticação
app.include_router(usuario_router)
app.include_router(cliente_router)