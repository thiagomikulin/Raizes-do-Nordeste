from main import bcrypt_context

from API.Schemas.Autenticacao.sUsuario import *

from Infrastructure.Repositories.base import Session
from Infrastructure.Models.Persona.mUsuario import *

from Domain.exceptions import ConflictExcept, NotFoundExcept, UnalteredExcept

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

    lista = sessao.query(Usuario).all()
    if id:
        lista = [item for item in lista if item.id == id]
        if lista == []:
            raise NotFoundExcept(id=id)
    if nome:
        lista = [item for item in lista if nome in item.nome]
        if lista == []:
            raise NotFoundExcept(nome=nome)
    if email:
        lista = [item for item in lista if email in item.email]
        if lista == []:
            raise NotFoundExcept(email=email)
    if cargo:
        lista = [item for item in lista if item.cargo in cargo]
        if lista == []:
            raise NotFoundExcept(cargo=cargo)
    elif not cargo:
        lista = [item for item in lista if (ator.cargo in item.cargo) or (ator.id == item.id)]
    if ativo:
        lista = [item for item in lista if item.ativo == ativo]
        if lista == []:
            raise NotFoundExcept(ativo=ativo)
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