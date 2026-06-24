from main import bcrypt_context

from API.Schemas.Persona.sUsuario import *

from Infrastructure.Repositories.base import Session
from Infrastructure.Models.Persona.mUsuario import *

from Domain.__exceptions__ import Conflito, NaoEncontrado, NaoAlterado

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def verificar_usuario_criacao(email, sessao:Session):
    usuario = sessao.query(Usuario).filter(Usuario.email == email).first()
    if usuario:
        raise Conflito('usuário', 'email', email)
    return

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def verificar_usuario_existe(sessao: Session, email=None, id=None):
    if email:
        usuario = sessao.query(Usuario).filter(Usuario.email == email).first()
    elif id:
        usuario = sessao.query(Usuario).filter(Usuario.id == id).first()
    else:
        raise 
    if not usuario:
        raise NaoEncontrado(campos={'email':email, 'id':id})
    return usuario

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def verificar_usuario_atualizacao(schema, usuario_bd):
    '''
    Verifica se há alguma diferença entre o usuário salvo e o schema enviado
    Se não houver diferença, a requisição retorna um erro 400, informando que a requisição é a mesma salva, portanto não será realizada
    '''
    campos = []
    if usuario_bd.nome != schema.nome:
        campos.append('nome')
    if usuario_bd.email != schema.email:
        campos.append('email')
    if usuario_bd.cargo != schema.cargo:
        campos.append('cargo')
    if len(campos) == 0:
        raise NaoAlterado(usuario_bd)
    
    return campos


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def criar_usuario_bd(schema: CriacaoSchema, sessao: Session):
    senha_criptografada = bcrypt_context.hash(schema.senha)
    novo_usuario = Usuario(schema.nome, schema.email, senha_criptografada, ativo=True, cargo='Não Classificado')
    sessao.add(novo_usuario)
    sessao.commit()
    return {
        'message': 'Usuário criado com sucesso!',
        "usuario":{
            "id": novo_usuario.id,
            "nome":novo_usuario.nome,
            "email":novo_usuario.email,
            "ativo": novo_usuario.ativo,
            "cargo": novo_usuario.cargo
        }

    }

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def buscar_usuarios(id, nome, email, cargo, ativo, sessao: Session, ator:Usuario=None, tipo=None):

    busca = sessao.query(Usuario)

    if id and id != 0:
        busca = busca.filter(Usuario.id == id)

    if nome:
        busca = busca.filter(Usuario.nome.contains(nome))

    if email:
        busca = busca.filter(Usuario.email.contains(email))
        
    if cargo:
        busca = busca.filter(Usuario.cargo == cargo)
        
    if ativo is not None:
        busca = busca.filter(Usuario.ativo == ativo)

    lista = busca.all()

    if not lista:
        raise NaoEncontrado(
            {
                "id":id,
                "nome":nome,
                "email":email,
                "cargo":cargo,
                "ativo":ativo
            }
        )
    return [
        {
            "id":item.id,
            "nome":item.nome,
            "email":item.email,
            "cargo":item.cargo,
            "ativo":item.ativo
        } for item in lista
    ]

def editar_usuario_bd(schema: EdicaoSchema, usuario: Usuario, campos: list, sessao: Session):
    if 'nome' in campos:
        usuario.nome = schema.nome
    if 'email' in campos:
        usuario.email = schema.email
    if 'cargo' in campos:
        usuario.cargo = schema.cargo
    sessao.commit()
    return {
        "message":"Edição realizada com sucesso!",
        "usuário":{
            campo:valor
            for campo, valor in schema.__dict__.items()
            if campo in campos
        }
    }

def ativar_usuario_bd(usuario: Usuario, sessao: Session):
    if usuario.ativo == True:
        raise NaoAlterado(usuario)
    else:
        usuario.ativo = True
        sessao.commit()
        return {
            "message": "usuário ativado com sucesso!",
            "usuário":{
                "id": usuario.id,
                "nome": usuario.nome,
                "ativo": usuario.ativo
            }
        }
    
def desativar_usuario_bd(usuario: Usuario, sessao: Session):
    if usuario.ativo == False:
        raise NaoAlterado(usuario)
    else:
        usuario.ativo = False
        sessao.commit()
        return {
            "message": "usuário desativado com sucesso!",
            "usuário":{
                "id": usuario.id,
                "nome": usuario.nome,
                "ativo": usuario.ativo
            }
        }
