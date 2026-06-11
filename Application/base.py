from fastapi import Depends, Request
import json
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from API.Routes.base import ExceptionHTTP

from main import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, oauth2_schema

#Infrastructure - Repositories
from Infrastructure.Repositories.reUsuario import *
from Infrastructure.Repositories.reCliente import *

#Infrastructure - Models


def criar_token(id, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc)+duracao_token
    dict_info = {
        "sub":str(id),
        "exp":data_expiracao
    }
    encoded_jwt =jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    #JWT
    #ID
    #data_expiracao #passou desse período, tem que gerar um novo
    return encoded_jwt

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def verificar_token(request: Request, token:str=Depends(oauth2_schema), sessao:Session=Depends(criar_sessao), model=Usuario):
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_user = int(dict_info.get('sub'))
    except JWTError as error:
        print(error)
        raise NaoAutenticado(request.url.path)
    ator = sessao.query(model).filter(model.id==id_user).first()
    if not ator:
        raise NaoEncontrado(request.url.path)
    elif ator.ativo == False:
        raise 

    return ator

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def verificar_permissao(ator, modulo, permissao):

    with open(f'./Domain/path_global.json', 'r', encoding='utf-8') as arquivo:
        caminhos = json.load(arquivo)
        rota = caminhos[modulo]

    with open(f'./Domain/{rota}', 'r', encoding='utf-8') as arquivo:
        dominio = json.load(arquivo)
        if type(ator) == Usuario:
            if ator.cargo not in dominio[permissao]:
                raise PermissionExcept
        elif type(ator) == Cliente:
            if 'cliente' not in dominio[permissao]:
                raise PermissionExcept

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Erros

class SchemaExcept(Exception):
    pass

class PermissionExcept(Exception):
    pass

class ConflictExcept(Exception):
    pass

class NotFoundExcept(Exception):
    pass

class IncorrectPWExcept(Exception):
    pass

#==============================================================================================

#Requisições diretas (dependem do Depends)
class NaoAutenticado(ExceptionHTTP):
    def __init__(self, path):
        super().__init__(
            code = 401,
            error="NÃO AUTENTICADO",
            message=f"É necessário estar autenticado para realizar esta ação!",
            detail=[
                {"field":"token","issue":"invalid token"}
            ],
            path=path
        )
    
class Desativado(ExceptionHTTP):
    def __init__(self, path):
        super().__init__(
            code=404,
            error='ACESSO INATIVO',
            message='Parece que seu acesso foi desativado! Entre em contato com a equipe técnica!',
            detail=[
                {"field":"ativo", "issue":"deactivated"}
            ],
            path=path
        )

class NaoEncontrado(ExceptionHTTP):
    def __init__(self, path):
        super().__init__(
            code=404,
            error='NÃO ENCONTRADO',
            message='Seu acesso não foi localizado em nosso sistema! Entre em contato com a equipe técnica!',
            detail=[
                {"field":"email", "issue":"not found"}
            ],
            path=path
        )

class AcessoInvalido(ExceptionHTTP):
    def __init__(self, path):
        super().__init__(
            code=401,
            error='ACESSO INVÁLIDO',
            message='Senha Incorreta! Tente novamente ou reinicie a senha!',
            detail=[
                {"field":"password", "issue":"incorrect"}
            ],
            path=path
        )