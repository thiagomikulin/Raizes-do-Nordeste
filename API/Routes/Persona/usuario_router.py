
from fastapi.security import OAuth2PasswordRequestForm

# Bases
from API.Routes.base import * #Exceptions HTTP apenas
from Application.base import verificar_permissao, verificar_token, timedelta, AcessoNaoEncontrado, NaoAutenticado
from Infrastructure.Repositories.base import criar_sessao, Session, Depends
from Application.base import criar_token

#Exceções (para tratar)
from Domain.exceptions import ExceptionHTTP, PermissionExcept, NotFoundExcept, ConflictExcept, IncorrectPWExcept, UnalteredExcept, SchemaInvalido, SemPermissao, Conflito, AcessoInvalido, ExceptionGenerica, NaoEncontrado, NaoAlterado

#Schema
from API.Schemas.Autenticacao.sUsuario import CriacaoSchema, LoginSchema, EdicaoSchema #Apenas Schemas

#Application
from Application.Persona.fUsuario import validar_schema_usuario_criar, validar_schema_usuario_editar, validar_schema_usuario_logar, autenticar_usuario, exec_busca
# from Application.Conectores.fUsuarioFilial import 

#Repositories - banco de dados
from Infrastructure.Repositories.Persona.reUsuario import criar_usuario_bd, verificar_usuario_criacao, editar_usuario_bd, verificar_usuario_existe, verificar_usuario_atualizacao
from Infrastructure.Repositories.Conectores.reUsuarioFilial import verificar_vinculo_filial

from Infrastructure.Models.Persona.mUsuario import Usuario

usuario_router = APIRouter(prefix='/usuarios', tags=['usuário'])

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Usuário - Criar (RF-U01)
@usuario_router.post('/criar', status_code=201)
async def criar_usuario(schema: CriacaoSchema, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    """
    Cria um novo usuário
    """
    # Para o uso inicial do sistema, deve ser utilizado o usuário master
    try:
        validar_schema_usuario_criar(schema) #Schema está ok?
        verificar_permissao(ator, 'usuario', 'criar', 'Não Classificado') #Ator tem permissão de criar?
        verificar_usuario_criacao(schema.email, sessao) #Usuário a ser criado já existe no sistema?
        criacao = criar_usuario_bd(schema, sessao) #Tentativa de criação
    except ExceptionHTTP:
        raise
    except Exception as e: 
        raise ExceptionGenerica(e) #apenas para tratativa de possíveis erros não mapeados
    else:
        return criacao

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Usuário - Listar (RF-U02)
@usuario_router.get('/')
async def listar_usuarios(
    id: int | None = 0,
    nome: str | None = None,
    email: str | None = None,
    cargo:str | None = None, 
    ativo: bool | None = True,
    filial: int | None = None,
    sessao: Session = 
    Depends(criar_sessao), 
    ator = Depends(verificar_token)
    ):

    try:
        tipo = verificar_permissao(ator, 'usuario' ,'buscar', cargo if cargo else None, id)
        lista = exec_busca(id, nome, email, cargo, ativo, filial, sessao, ator, tipo)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    return lista

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Usuário - Atualizar (RF-U03)
@usuario_router.put('/{id}')
async def atualizar_usuario(id: int, schema: EdicaoSchema,  sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    path = f'/usuarios/{str(id)}'
    try:
        validar_schema_usuario_editar(schema) #O schema está correto?
        verificar_permissao(ator, 'usuario', 'editar', schema.cargo) #O usuário pode editar outro?
        verificar_usuario_existe(schema.email, sessao)
        verificar_usuario_atualizacao(id, schema, sessao)
        edicao = editar_usuario_bd(schema, sessao)
    except NotFoundExcept as e:
        raise NaoEncontrado(path, e.campos)
    except UnalteredExcept:
        raise NaoAlterado
    else:
        return edicao

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

@usuario_router.put('/{id}/ativar')
async def ativar_usuario():
    pass

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

@usuario_router.put('/{id}/desativar')
async def desativar_usuario():
    pass


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

@usuario_router.post('/login')
async def login(schema: LoginSchema, sessao:Session = Depends(criar_sessao)):
    path='/usuarios/login'
    try:
        validar_schema_usuario_logar(schema)
        usuario = autenticar_usuario(schema.email, schema.senha, sessao)
    except NotFoundExcept:
        raise AcessoNaoEncontrado(path)
    except IncorrectPWExcept:
        raise AcessoInvalido(path)
    else:
        access_token = criar_token(usuario.id, Usuario)
        refresh_token = criar_token(usuario.id, Usuario, duracao_token=timedelta(days=7))
        return {
            'access-token':access_token,
            "refresh_token":refresh_token,
            "token_type":"Bearer"
        }

#--------------------------

@usuario_router.post('/login-form')
async def login_form(dados_formulario:OAuth2PasswordRequestForm = Depends(), sessao:Session=Depends(criar_sessao)):
    path = '/usuarios/login-form'
    try:
        usuario = autenticar_usuario(email=dados_formulario.username, senha=dados_formulario.password, sessao=sessao)
    except Exception as e:
        raise NaoEncontrado(path, e.campos)
    #OBS: tem que ter validação de senha também!!!!!!!!!
    else:
        access_token = criar_token(usuario.id, Usuario)
        return {
            "access_token":access_token,
            "token_type":"Bearer"
            }

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Desautenticar
@usuario_router.post('/logout')
async def logout():
    pass
    #Pega o token e muda o limite para o horário atual

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

@usuario_router.post('/refresh')
async def refresh_token():
    pass
    #Pega o refresh_token e entrega um token normal
    
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

@usuario_router.post('/reset_senha')
async def reset_senha():
    pass
    #Recebe o usuário autenticado e envia um request de troca de senha para o email
    #Se não tiver email cadastrado, retorna erro e indica para contatar equipe técnica

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

@usuario_router.post('/{id}/filiais/{filial}/vincular')
async def vincular_filial(id: int=0, filial:int=0, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    path = '/usuarios/login-form'
    try:
        usuario = verificar_usuario_existe(id=id, sessao=sessao)
        verificar_vinculo_filial(id_usuario = id, id_filial = filial, sessao=sessao)
        verificar_permissao(ator, 'usuario', 'associar', usuario.cargo)
        vinculo = criar_vinculo_usufil_bd(usuario.id, filial)
    except ConflictExcept:
        raise Conflito('Vínculo', 'Usuário/Filial', f'{id}/{filial}', path)
    except PermissionExcept:
        raise SemPermissao(ator)
    except Exception as e:
        raise ExceptionGenerica(e, path)
    else:
        return 
        

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

@usuario_router.post('/{id}/filiais/desvincular')
async def desvincular_filial():
    pass

        
