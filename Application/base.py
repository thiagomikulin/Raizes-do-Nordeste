#Módulos externos
from fastapi import Depends, Request # type: ignore
import json
from jose import jwt, JWTError  # type: ignore
from datetime import datetime, timedelta, timezone

#Secrets
from main import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, SECRET_KEY_REFRESH, ALGORITHM, oauth2_schema

#Exceções
from Domain.exceptions import NaoAutenticado, AcessoNaoEncontrado, NaoAtivo, SemPermissao

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
    #Validação se é refresh_token
    if duracao_token == timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES): #Access
        dict_info = {
            "sub":str(id),
            "exp":data_expiracao,
            "roles":tipo.__name__
        }
        encoded_jwt =jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    else: #Refresh
        dict_info = {
            "sub":str(id),
            "exp":data_expiracao,
            "roles":tipo.__name__
        }
        encoded_jwt =jwt.encode(dict_info, SECRET_KEY_REFRESH, ALGORITHM)
    #JWT
    #ID
    #data_expiracao #passou desse período, tem que gerar um novo
    return encoded_jwt

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def verificar_token(request: Request, token:str=Depends(oauth2_schema), sessao:Session=Depends(criar_sessao)):
    try:
        if request.url.path == '/usuarios/refresh' or request.url.path == '/clientes/refresh':
            dict_info = jwt.decode(token, SECRET_KEY_REFRESH, ALGORITHM)
        else:
            dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_user = int(dict_info.get('sub'))
        tipo = dict_info.get('roles')
    except JWTError as error:
        print(error)
        raise NaoAutenticado()
    except:
        raise NaoAutenticado()
    if tipo == "Usuario":
        ator = sessao.query(Usuario).filter(Usuario.id==id_user).first()
    elif tipo == "Cliente":
        ator = sessao.query(Cliente).filter(Cliente.id==id_user).first()
    if not ator:
        raise AcessoNaoEncontrado()
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
        if type(ator) == Usuario: #se for usuário
            if ator.cargo not in dominio[permissao]: #se o cargo não estiver na permissão, retorna erro!
                raise SemPermissao(ator=ator, permissao=permissao)
            else:
                if type(dominio[permissao]) != list: #se for um formato customizado (além de listagem, com customização de tipo)
                    if (id != 0 and id) and ator.id == id: #se tiver um id filtrado e o id do ator for igual, retorna o domínio para o cargo (filtro no bd)
                        return dominio[permissao][ator.cargo]
                    elif (id == 0 or not id): #se não filtrar por dominio, também retorna
                        return dominio[permissao][ator.cargo]
                    elif tipo not in dominio[permissao][ator.cargo] and tipo != None and not id: #Se o tipo de entidade a ser modificada não estiver na lista, tiver tipo e não tiver id (pra não filtrar pelo usuário próprio)
                        raise SemPermissao(ator)
                    else:
                        return dominio[permissao][ator.cargo]
                else:
                    return TypeError
        elif type(ator) == Cliente:
            if 'Cliente' not in dominio[permissao]:
                raise SemPermissao(ator)



