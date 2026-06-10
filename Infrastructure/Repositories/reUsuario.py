from main import bcrypt_context

from Application.base import *

from Infrastructure.Repositories.base import *
from Infrastructure.Models.Persona.mUsuario import *

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def verificar_usuario_criacao(email, sessao:Session):
    usuario = sessao.query(Usuario).filter(Usuario.email == email).first()
    if usuario:
        return 409
    return usuario

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def verificar_usuario_existe(email, sessao: Session):
    usuario = sessao.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return 404
    return usuario

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def criar_usuario_bd(nome, email, senha, sessao: Session):
    print('teste')
    senha_criptografada = bcrypt_context.hash(senha)
    novo_usuario = Usuario(nome, email, senha_criptografada, ativo=True, cargo='Não Classificado')
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