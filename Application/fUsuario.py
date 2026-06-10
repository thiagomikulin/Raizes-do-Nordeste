import json

from Application.base import *

#API - Schemas
from API.Schemas.usuario_schema import *

from Infrastructure.Repositories.reUsuario import *

with open('./Domain/Persona/Usuario.json', 'r', encoding='utf-8') as arquivo:
    dominio = json.load(arquivo)

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def validar_schema_usuario_criar(schema: CriacaoSchema):
    if not schema.nome or not schema.email or not schema.senha:
        raise SchemaExcept
    
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def validar_schema_usuario_logar(schema: LoginSchema):
    if not schema.email or not schema.senha:
        return False
    else:
        return True

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def autenticar_usuario(email: str, senha: str, sessao: Session):
    usuario = verificar_usuario_existe(email, sessao)
    if type(usuario) != Usuario:
        #Este usuário não existe
        return 404
    elif not bcrypt_context.verify(senha, usuario.senha):
        return 403
    return usuario

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def verificar_token_usuario(request: Request, token:str=Depends(oauth2_schema), sessao:Session=Depends(criar_sessao)):
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_user = int(dict_info.get('sub'))
    except JWTError as error:
        print(error)
        raise NaoAutenticado(request.url.path)
    usuario = sessao.query(Usuario).filter(Usuario.id==id_user).first()
    if not usuario or usuario.ativo == False:
        raise NaoEncontrado(request.url.path)
    return usuario

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def exec_busca(id, nome, email, cargo, sessao: Session, usuario: Usuario):
    if usuario.cargo not in dominio['buscar']:
        return 403
    return buscar_usuarios(id, nome, email, cargo, sessao)