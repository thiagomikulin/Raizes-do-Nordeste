#Módulos externos
from fastapi import Depends, Request # type: ignore
import json
from jose import jwt, JWTError  # type: ignore
from datetime import datetime, timedelta, timezone

#Secrets
from main import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, SECRET_KEY_REFRESH, ALGORITHM, oauth2_schema

#Exceções
from Domain.__exceptions__ import NaoAlterado, NaoAutenticado, AcessoNaoEncontrado, NaoAtivo, SemPermissao

#Bases
from Infrastructure.Repositories.base import Session, criar_sessao

#Infrastructure - Repositories
from Infrastructure.Repositories.Persona.reUsuario import Usuario
from Infrastructure.Repositories.Persona.reCliente import Cliente


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

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

def verificar_permissao(ator, permissao: str, modulo:str, tipo: str=None):
    '''
    ator - o acesso que modifica
    modulo - a tabela que modifica
    permissao - o que pode fazer
    tipo - em que tipo de entidade pode editar
    id - identificador do que está sendo alterado (opcional)
    '''

    #A rota poderá receber o cargo do ator se for a criação de um usuário.
    #A disposição das hierarquias está organizada de acordo com os índices da lista
    #Se o índice do cargo for menor que o índice do ator (cargo "menor"), permite realizar, senão retorna erro

    #Define o domínio com base no ator
    if isinstance(ator, Usuario):
        dominio = ator.cargo.name.replace(' ','')
    else:
        dominio = 'Cliente'

    with open(f"./Domain/{dominio}.json", encoding='utf-8') as arquivo:
        permissoes = json.load(arquivo)

    #Verifica se o domínio do ator abarca a permissão
    if permissao not in permissoes:
        raise SemPermissao(ator=ator, permissao=permissao)
    
    
    #Suplementa o tipo se tiver (EX: Usuario - Atendente)
    if tipo is not None:
        modulo += f" - {tipo}" if '-' not in modulo else '' #Suplemento para evitar acúmulo de tipo
        return [permissoes[permissao].index(modulo)]
    elif tipo is None and modulo == 'Usuario':
        indice_dominio = permissoes[permissao].index(f'{modulo} - {dominio}')
        return permissoes[permissao][0:indice_dominio]

def verificar_entidade_atualizacao(schema, entidade):
    print('schema', schema)
    print('entidade', entidade)
    campos = []
    dict_ent = entidade.__dict__
    print('dict_ent',dict_ent)
    for chave, valor in schema.__dict__.items():
        coluna = dict_ent[chave]
        print('coluna', coluna)
        if coluna != valor:
            campos.append(chave)
    if len(campos) == 0:
        raise NaoAlterado(entidade, dict_ent)
        #coluna = getattr(entidade, item)
    print(campos)
    return campos