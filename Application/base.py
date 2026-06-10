from fastapi import Depends, Request

from API.Routes.base import ExceptionHTTP

from datetime import datetime, timedelta, timezone
from main import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, oauth2_schema
from jose import jwt, JWTError


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