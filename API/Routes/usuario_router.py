
#API
from API.Routes.base import *
from API.Schemas.usuario_schema import *

from Application.fUsuario import *

usuario_router = APIRouter(prefix='/usuarios', tags=['usuário'])

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

@usuario_router.post('/criar', status_code=201)
async def criar_usuario(schema: CriacaoSchema, sessao: Session = Depends(criar_sessao), usuario: Usuario=Depends(verificar_token_usuario)):
    """
    Cria um novo usuário
    """
    # Para o uso inicial do sistema, deve ser utilizado o usuário master

    #O Schema está correto?
    try:
        validar_schema_usuario_criar(schema)
        verificar_permissao(usuario, 'criar')
    except SchemaExcept:
        pass
    except PermissionExcept:
        pass
    except ConflictExcept:
        pass
    if not validar_schema_usuario_criar(schema):
        raise SchemaInvalido(schema, '/usuarios/criar')
    
    #------------------------

        verificar_permissao()
    if usuario == 403:
        raise ExceptionHTTP(
            code = 403,
            error="NÃO AUTORIZADO",
            message="Parece que você não tem acesso para criar um usuário! Entre em contato com seu administrador!",
            detail=[
                {"field":"cargo","issue":"not authorized"}
            ],
            path='/usuarios/criar'
        )
        
    #------------------------

    #Usuário existe?
    if verificar_usuario_criacao(schema.email, sessao) == 409:
        raise ExceptionHTTP(
                code = 409,
                error=f"CONFLITO DE USUÁRIO",
                message=f"Já existe um usuário com e-mail {schema.email} cadastrado no sistema",
                detail=[
                    {"field":"email","issue":"duplicated value"}
                ],
                path='/usuarios/criar'
            )
    
    #------------------------

    return criar_usuario_bd(schema.nome, schema.email, schema.senha, sessao)

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

@usuario_router.post('/login')
async def login(schema: LoginSchema, sessao:Session = Depends(criar_sessao)):
    usuario = autenticar_usuario(schema.email, schema.senha, sessao)
    if type(usuario) != Usuario:
        if usuario == 404:
            raise ExceptionHTTP(
                    code = 404,
                    error='USUÁRIO INVÁLIDO!',
                    message='Este usuário não existe',
                    detail=[
                        {"field":"email","issue":"not found"}
                    ],
                    path='/usuarios/criar'
                )
        elif usuario == 403:
            raise ExceptionHTTP(
                    code = 403,
                    error='CREDENCIAIS INVÁLIDAS!',
                    message='Credenciais inválidas',
                    detail=[
                        {"field":"email","issue":"not found"}
                    ],
                    path='/usuarios/criar'
                )

    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            'access-token':access_token,
            "refresh_token":refresh_token,
            "token_type":"Bearer"
        }

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

@usuario_router.get('/')
async def listar_usuarios(id: int = 0,nome: str = None,email: str = None,cargo:str = None, sessao: Session = Depends(criar_sessao), usuario: Usuario = Depends(verificar_token_usuario)):
    if type(usuario) != Usuario:
        if usuario == 404:
            raise ExceptionHTTP(
                    code = 404,
                    error='USUÁRIO INVÁLIDO!',
                    message='Este usuário não existe',
                    detail=[
                        {"field":"email","issue":"not found"}
                    ],
                    path='/usuarios/criar'
                )
        elif usuario == 401:
            raise ExceptionHTTP(
                    code = 401,
                    error='CREDENCIAIS INVÁLIDAS!',
                    message='Credenciais inválidas',
                    detail=[
                        {"field":"email","issue":"not found"}
                    ],
                    path='/usuarios/criar'
                )
    lista = exec_busca(id, nome, email, cargo, sessao, usuario)
    if type(lista) != list:
        if lista == 403:
            raise ExceptionHTTP(
                code = 403,
                error='CREDENCIAIS INVÁLIDAS!',
                message='Credenciais inválidas',
                detail=[
                    {"field":"email","issue":"not found"}
                ],
                path='/usuarios/criar'
            )
    return


        
    
    
    
        
