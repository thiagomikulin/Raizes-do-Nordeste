#Módulos externos
from fastapi import Depends, Request # type: ignore
import json
from jose import jwt, JWTError  # type: ignore
from datetime import datetime, timedelta, timezone

#Secrets
from main import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, oauth2_schema

#Exceções
from Domain.exceptions import NaoAutenticado, NaoEncontrado

#Bases
from Infrastructure.Repositories.base import Session, criar_sessao

#Infrastructure - Repositories
from Infrastructure.Repositories.reUsuario import Usuario
from Infrastructure.Repositories.reCliente import Cliente

#Infrastructure - Models

#Infrastructure - 

#Application - exceptions
from Domain.exceptions import PermissionExcept

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
    except:
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



