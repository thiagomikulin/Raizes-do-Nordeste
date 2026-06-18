#Módulos externos
from fastapi import Depends, Request # type: ignore
import json
from jose import jwt, JWTError  # type: ignore
from datetime import datetime, timedelta, timezone

#Secrets
from main import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, oauth2_schema

#Exceções
from Domain.exceptions import NaoAutenticado, AcessoNaoEncontrado, NaoAtivo

#Bases
from Infrastructure.Repositories.base import Session, criar_sessao

#Infrastructure - Repositories
from Infrastructure.Repositories.Persona.reUsuario import Usuario
from Infrastructure.Repositories.Persona.reCliente import Cliente

#Infrastructure - Models

#Infrastructure - 

#Application - exceptions
from Domain.exceptions import PermissionExcept

def criar_token(id, tipo, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc)+duracao_token
    dict_info = {
        "sub":str(id),
        "exp":data_expiracao,
        "roles":tipo.__name__
    }
    encoded_jwt =jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    #JWT
    #ID
    #data_expiracao #passou desse período, tem que gerar um novo
    return encoded_jwt

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def verificar_token(request: Request, token:str=Depends(oauth2_schema), sessao:Session=Depends(criar_sessao)):
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_user = int(dict_info.get('sub'))
        tipo = dict_info.get('roles')
    except JWTError as error:
        print(error)
        raise NaoAutenticado(request.url.path)
    except:
        raise NaoAutenticado(request.url.path)
    if tipo == "Usuario":
        ator = sessao.query(Usuario).filter(Usuario.id==id_user).first()
    elif tipo == "Cliente":
        ator = sessao.query(Cliente).filter(Cliente.id==id_user).first()
    if not ator:
        raise AcessoNaoEncontrado(request.url.path)
    elif ator.ativo == False:
        raise NaoAtivo
    return ator

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def verificar_permissao(ator, modulo:str, permissao:str, tipo: str=None, id:int=0):
    '''
    ator - o acesso que modifica
    modulo - a tabela que modifica
    permissao - o que pode fazer
    tipo - em que tipo de entidade pode editar
    id - identificador do que está sendo alterado (opcional)
    '''

    with open(f"./Domain/path_global.json", 'r', encoding='utf-8') as arquivo:
        caminhos = json.load(arquivo)
        rota = caminhos[modulo]

    with open(f"./Domain{rota}", 'r', encoding='utf-8') as arquivo:
        dominio = json.load(arquivo)
        if type(ator) == Usuario:
            if ator.cargo not in dominio[permissao]:
                raise PermissionExcept
            else:
                if type(dominio[permissao]) != list:
                    if id != 0 and ator.id == id:
                        return dominio[permissao][ator.cargo]
                    elif id == 0:
                        return dominio[permissao][ator.cargo]
                    elif tipo not in dominio[permissao][ator.cargo] and tipo != None and not id:
                        raise PermissionExcept
                    else:
                        return dominio[permissao][ator.cargo]
                else:
                    return TypeError
        elif type(ator) == Cliente:
            if 'Cliente' not in dominio[permissao]:
                raise PermissionExcept



