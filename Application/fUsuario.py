import json

from Application.base import *

#API - Schemas
from API.Schemas.usuario_schema import *

from Infrastructure.Repositories.reUsuario import *

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

def verificar_token_usuario(request: Request, token:str=Depends(oauth2_schema), sessao:Session=Depends(criar_sessao)):
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_user = int(dict_info.get('sub'))
    except JWTError as error:
        print(error)
        raise NaoAutenticado(request.url.path)
    usuario = sessao.query(Usuario).filter(Usuario.id==id_user).first()
    if not usuario:
        raise NaoEncontrado(request.url.path)
    elif usuario.ativo == False:
        raise 

    return usuario

def verificar_permissao_usu(usuario:Usuario, modulo, permissao):

    with open(f'./Domain/path_global.json', 'r', encoding='utf-8') as arquivo:
        caminhos = json.load(arquivo)
        rota = caminhos[modulo]

    with open(f'./Domain/{rota}', 'r', encoding='utf-8') as arquivo:
        dominio = json.load(arquivo)
        if usuario.cargo not in dominio[permissao]:
            raise PermissionExcept


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def exec_busca(id, nome, email, cargo, sessao: Session, usuario: Usuario):
    return buscar_usuarios(id, nome, email, cargo, sessao)
