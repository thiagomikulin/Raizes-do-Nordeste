from Application.base import *

#API - Schemas
from API.Schemas.usuario_schema import *

from Infrastructure.Repositories.reUsuario import *

def validar_schema_usuario_criar(schema: CriacaoSchema):
    if not schema.nome or not schema.email or not schema.senha:
        return False
    else:
        return True
    
def validar_schema_usuario_logar(schema: LoginSchema):
    if not schema.email or not schema.senha:
        return False
    else:
        return True

def autenticar_usuario(email: str, senha: str, sessao: Session):
    usuario = verificar_usuario_existe(email, sessao)
    if type(usuario) != Usuario:
        #Este usuário não existe
        return [404, 'USUÁRIO INVÁLIDO!','Este usuário não existe']
    elif not bcrypt_context.verify(senha, usuario.senha):
        return ['CREDENCIAIS INVÁLIDAS!','Credenciais inválidas']
    return usuario