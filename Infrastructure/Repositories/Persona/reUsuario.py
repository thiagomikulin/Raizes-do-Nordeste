from main import bcrypt_context

from API.Schemas.Autenticacao.sUsuario import *

from Infrastructure.Repositories.base import Session
from Infrastructure.Models.Persona.mUsuario import *

from Domain.exceptions import Conflito, NaoEncontrado, UnalteredExcept

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
        raise NaoEncontrado()
    return usuario

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def verificar_usuario_atualizacao(id, schema, sessao):
    '''
    Verifica se há alguma diferença entre o usuário salvo e o schema enviado
    Se não houver diferença, a requisição retorna um erro 400, informando que a requisição é a mesma salva, portanto não será realizada
    '''
    usuario_bd = sessao.query(Usuario).filter(Usuario.id == id).first()
    if usuario_bd.nome == schema.nome and usuario_bd.email == schema.email and usuario_bd.cargo == schema.cargo:
        raise UnalteredExcept

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
        print(nome)
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

def editar_usuario_bd(schema: EdicaoSchema, sessao: Session):
    return 'teste'