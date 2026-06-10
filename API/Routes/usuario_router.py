
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

    path='/usuarios/criar'
    try:
        validar_schema_usuario_criar(schema) #Schema está ok?
        verificar_permissao_usu(usuario, 'usuario', 'criar') #Usuário tem permissão de criar?
        verificar_usuario_criacao(schema.email, sessao) #Usuário existe?
        criacao = criar_usuario_bd(schema.nome, schema.email, schema.senha, sessao) #Tentativa de criação
    except SchemaExcept: 
        raise SchemaInvalido(schema, path)
    except PermissionExcept:
        raise SemPermissao(path)
    except ConflictExcept:
        raise Conflito(entidade='usuário', campo='e-mail', valor_campo=schema.email, path=path)
    else:
        return criacao

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

@usuario_router.post('/login')
async def login(schema: LoginSchema, sessao:Session = Depends(criar_sessao)):
    path='/usuarios/login'
    try:
        usuario = autenticar_usuario(schema.email, schema.senha, sessao)
    except NotFoundExcept:
        raise NaoEncontrado(path)
    except IncorrectPWExcept:
        raise AcessoInvalido(path)
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
    try:
        verificar_permissao_usu(usuario, 'usuario' ,'buscar')
        lista = exec_busca(id, nome, email, cargo, sessao, usuario)
    except PermissionExcept:
        raise SemPermissao('/')
    return lista


        
    
    
    
        
