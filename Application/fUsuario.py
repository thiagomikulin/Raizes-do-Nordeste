
#Application
from Application.base import *

#API - Schemas
from API.Schemas.sUsuario import *

#Infrastructure
from Infrastructure.Repositories.reUsuario import *
from Infrastructure.Repositories.reCliente import *

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def validar_schema_usuario_criar(schema: CriacaoSchema):
    if (not schema.nome) or (not schema.email) or (not schema.senha):
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






#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def exec_busca(id, nome, email, cargo, sessao: Session, usuario: Usuario):
    return buscar_usuarios(id, nome, email, cargo, sessao)
