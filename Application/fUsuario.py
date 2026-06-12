
#Application
from Application.base import *

#API - Schemas
from API.Schemas.Autenticacao.sUsuario import *

#Infrastructure
from Infrastructure.Repositories.Autenticacao.reUsuario import *
from Infrastructure.Repositories.Autenticacao.reCliente import *

from Domain.exceptions import SchemaExcept, IncorrectPWExcept

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def validar_schema_usuario_criar(schema: CriacaoSchema):
    if (not schema.nome) or (not schema.email) or (not schema.senha):
        raise SchemaExcept

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def validar_schema_usuario_editar(schema: EdicaoSchema):
    if (not schema.nome) or (not schema.email) or (not schema.cargo):
        raise SchemaExcept
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def validar_schema_usuario_logar(schema: LoginSchema):
    if not schema.email or not schema.senha:
        raise SchemaExcept

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def autenticar_usuario(email: str, senha: str, sessao: Session):
    try:
        usuario = verificar_usuario_existe(email, sessao)
        if not bcrypt_context.verify(senha, usuario.senha):
            raise IncorrectPWExcept
    except NotFoundExcept:
        raise NotFoundExcept
    except IncorrectPWExcept:
        raise IncorrectPWExcept
    else:
        return usuario

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def exec_busca(id, nome, email, cargo, ativo, sessao: Session, usuario: Usuario, tipo=None):
    #Se tiver algum filtro, e o filtro não for validado, levanta NotFoundException
    lista = buscar_usuarios(id, nome, email, cargo, ativo, sessao, usuario, tipo)
    ator_na_lista = [item for item in lista if item['id'] == usuario.id]
    print(ator_na_lista)
    if ator_na_lista != []:
        return ator_na_lista
    elif cargo not in tipo:
        raise PermissionExcept
    return lista
