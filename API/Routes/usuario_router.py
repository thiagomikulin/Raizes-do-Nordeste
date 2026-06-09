from API.Routes.base import *

#API - Schemas
from API.Schemas.usuario_schema import *

from Application.fUsuario import *

usuario_router = APIRouter(prefix='/usuarios', tags=['usuário'])

@usuario_router.post('/criar')
async def criar_usuario(schema: CriacaoSchema, sessao: Session = Depends(criar_sessao)):
    # usuario: Usuario=Depends(verificar_token)
    """
    Cria um novo usuário
    """
    # Para o uso inicial do sistema, deve ser utilizado o usuário master
    #O Schema está correto?
    if not validar_schema_usuario_criar(schema):
        raise ExceptionHTTP(
            code=400, 
            error='CAMPOS PREENCHIDOS INCORRETAMENTE',
            message="Os campos não foram preenchidos corretamente! Verifique e tente novamente",
            detail=[{"field":attr, "issue":"required"} for attr, val in schema.__dict__.items() if not val], #Retorna o atributo na lista de atributos e valores se o valor não existir
            path='/usuarios/criar'
        )
    #AUTORIZAÇÃO
    #Verificação de existência de usuário criador e credenciais
    # check_token = verificar_token(schema.email, schema.senha)
    # if type(check_token) != Usuario:
    #     if check_token == 401:
    #         raise ExceptionHTTP(
    #             code = 401,
    #             error="NÃO AUTENTICADO",
    #             message="É necessário estar autenticado para criar um usuário!",
    #             detail=[
    #                 {"field":"token","issue":"invalid token"}
    #             ],
    #             path='/usuarios/criar'
                
    #         )
    #     elif check_token == 402:
    #         raise ExceptionHTTP(
    #             code = 402,
    #             error="NÃO AUTORIZADO",
    #             message="Parece que você não tem acesso para criar um usuário! Entre em contato com seu administrador!",
    #             detail=[
    #                 {"field":"cargo","issue":"not authorized"}
    #             ],
    #             path='/usuarios/criar'
    #         )
    if verificar_usuario(schema.email, sessao) == 409:
        raise ExceptionHTTP(
                code = 409,
                error=f"CONFLITO DE USUÁRIO",
                message=f"Já existe um usuário com e-mail {schema.email} cadastrado no sistema",
                detail=[
                    {"field":"email","issue":"duplicated value"}
                ],
                path='/usuarios/criar'
            )
    
    return criar_usuario_bd(schema.nome, schema.email, schema.senha, sessao)

@usuario_router.post('/login')
async def login(schema: LoginSchema, sessao:Session = Depends(criar_sessao)):
    usuario = autenticar_usuario(schema.email, schema.senha, sessao)
    if type(usuario) != Usuario:
        raise ExceptionHTTP(
                code = usuario[0],
                error=usuario[1],
                message=usuario[2],
                detail=[
                    {"field":"email","issue":"duplicated value"}
                ],
                path='/usuarios/criar'
            )
    return {'teste':'teste'}



        
    
    
    
        
