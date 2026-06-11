from main import bcrypt_context

from API.Schemas.sUsuario import *

from Infrastructure.Repositories.base import Session
from Infrastructure.Models.Persona.mUsuario import *

from Domain.exceptions import ConflictExcept, NotFoundExcept

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def verificar_usuario_criacao(email, sessao:Session):
    usuario = sessao.query(Usuario).filter(Usuario.email == email).first()
    if usuario:
        raise ConflictExcept
    return usuario

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def verificar_usuario_existe(email, sessao: Session):
    usuario = sessao.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise NotFoundExcept
    return usuario

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
def buscar_usuarios(id, nome, email, cargo, sessao: Session):
    lista = sessao.query(Usuario).all()
    return lista