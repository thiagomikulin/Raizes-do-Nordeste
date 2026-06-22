
#Requisito único

from fastapi.security import OAuth2PasswordRequestForm

# Bases
from API.Routes.base import *
from Application.base import verificar_permissao, verificar_token, timedelta, AcessoNaoEncontrado, NaoAutenticado
from Infrastructure.Repositories.base import criar_sessao, Session, Depends
from Application.base import criar_token
#Exceções (para tratar)
from Domain.__exceptions__ import ExceptionHTTP, ExceptionGenerica

from Application.chamada_rota import ativar_entidade, criar_entidade, desativar_entidade, editar_entidade, excluir_entidade, visualizar_entidade



#Requisitos
from API.Schemas.Persona.sUsuario import CriacaoSchema, LoginSchema, EdicaoSchema #Apenas Schemas
from Application.Persona.fUsuario import validar_schema_usuario_criar, validar_schema_usuario_editar, validar_schema_usuario_logar, autenticar_usuario, exec_busca
from Infrastructure.Repositories.Persona.reUsuario import criar_usuario_bd, verificar_usuario_criacao, editar_usuario_bd, verificar_usuario_existe, verificar_usuario_atualizacao, ativar_usuario_bd, desativar_usuario_bd
from Infrastructure.Models.Persona.mUsuario import Usuario
from Infrastructure.Models.Conectores.mUsuarioFilial import UsuarioFilial


#Complementares
from Infrastructure.Repositories.Conectores.reUsuarioFilial import verificar_vinculo_filial, vincular_filial_bd, desvincular_filial_bd, verificar_vinculo_filial_desv

from API.Schemas.Conectores.sUsuarioFilial import sUsuarioFilialCriacao, sUsuarioFilialExclusao

from Infrastructure.Repositories.Empresa.reFilial import verificar_filial_existe
from Infrastructure.Integracoes.email import solicitar_reset_senha

usuario_router = APIRouter(prefix='/usuarios', tags=['usuário'])

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Usuário - Criar (RF-U01)
@usuario_router.post('/criar', status_code=201)
async def criar_usuario(schema: CriacaoSchema, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    """
    Cria um novo usuário
    Todos os usuários criados serão inicializados com cargo "Não Classificado"
    """
    # Para o uso inicial do sistema, deve ser utilizado o usuário master
    try:
        usuario = criar_entidade(Usuario, schema, ator, sessao, campo_verificacao=['email'])
    except ExceptionHTTP:
        raise
    except Exception as e: 
        raise ExceptionGenerica(e) #apenas para tratativa de possíveis erros não mapeados
    else:
        return usuario

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Usuário - Listar (RF-U02)
@usuario_router.get('/')
async def listar_usuarios(
    id: int | None = None,
    nome: str | None = None,
    email: str | None = None,
    cargo:str | None = None, 
    ativo: bool | None = True,
    filial: int | None = None,
    sessao: Session = 
    Depends(criar_sessao), 
    ator = Depends(verificar_token)
    ):
    """
    Listar usuários de acordo com o filtro
    OBS: a visualização dos dados se limita à filial na qual trabalham, e possui restrições por cargo (exceto para Gerente e TI)
    """
    dict_campos = {
        'id':id,
        'nome':nome,
        'email':email,
        'cargo':cargo,
        'ativo':ativo,
        'filial':filial
    }
    try:
        lista = visualizar_entidade(Usuario, sessao, ator, dict_campos)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    return lista

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Usuário - Atualizar (RF-U03)
@usuario_router.put('/{id}')
async def atualizar_usuario(id: int, schema: EdicaoSchema,  sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    """
    Atualizar dados de usuários (a partir do schema para edição)
    OBS: Gerentes poderão atualizar usuários de todos os cargos, menos outros gerentes
    """
    try:
        edicao = editar_entidade(id, Usuario, schema, ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return edicao

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Usuário - Ativar (RF-U04)
@usuario_router.patch('/{id}/ativar')
async def ativar_usuario(id: int, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        usuario_ativo = ativar_entidade(Usuario, ator, id, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return usuario_ativo

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Usuário - Desativar (RF-U04)
@usuario_router.patch('/{id}/desativar')
async def desativar_usuario(id: int, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        usuario_desativo = desativar_entidade(Usuario, ator, id, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return usuario_desativo



#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Usuário - Autenticar(RF-U05)
@usuario_router.post('/login')
async def login(schema: LoginSchema, sessao:Session = Depends(criar_sessao)):
    try:
        validar_schema_usuario_logar(schema)
        usuario = autenticar_usuario(schema.email, schema.senha, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        access_token = criar_token(usuario.id, Usuario)
        refresh_token = criar_token(usuario.id, Usuario, duracao_token=timedelta(days=7))
        return {
            'access_token':access_token,
            "refresh_token":refresh_token,
            "token_type":"Bearer"
        }

#--------------------------

#Usuário - Autenticar(RF-U05)
@usuario_router.post('/login-form', include_in_schema=False)
async def login_form(dados_formulario:OAuth2PasswordRequestForm = Depends(), sessao:Session=Depends(criar_sessao)):
    try:
        usuario = autenticar_usuario(email=dados_formulario.username, senha=dados_formulario.password, sessao=sessao)
    except Exception as e:
        raise ExceptionGenerica(e)
    #OBS: tem que ter validação de senha também!!!!!!!!!
    else:
        access_token = criar_token(usuario.id, Usuario)
        return {
            "access_token":access_token,
            "token_type":"Bearer"
            }

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Usuário - Atualizar token (RF-U06)
@usuario_router.post('/refresh')
async def refresh_token(ator=Depends(verificar_token)):
    ac = criar_token(ator.id, Usuario)
    return {
        "access_token":ac,
        "token_type":"Bearer"
    }
    #Pega o refresh_token e entrega um token normal
    
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Usuário - Solicitar Reset Senha (RF-U07)
@usuario_router.post('/reset_senha')
async def reset_senha(email: str, sessao: Session = Depends(criar_sessao)):
    try:
        verificar_usuario_existe(email=email, sessao=sessao)
        reset = solicitar_reset_senha(email)
        #OBS: O ENVIO DE SOLICITAÇÃO NÃO SERÁ REGISTRADO EM LOG, MAS A ALTERAÇÃO EFETIVA, QUANDO IMPLEMENTADA, REGISTRARÁ
        #Recebe o usuário autenticado e envia um request de troca de senha para o email
        #Se não tiver email cadastrado, retorna erro e indica para contatar equipe técnica
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return reset

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Usuário - Associar a filial (RF-U08)
@usuario_router.post('/{usuario}/filiais/{filial}/vincular')
async def vincular_filial(id: int=0, id_filial:int=0, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    schema = sUsuarioFilialCriacao(**{'usuario':id, 'filial':id_filial})
    try:
        vinculo = criar_entidade(UsuarioFilial, schema, ator, sessao, ['usuario', 'filial'])
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return vinculo
        

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Usuário - Desassociar a filial (RF-U09)
@usuario_router.delete('/{id}/filiais/{id_filial}/desvincular')
async def desvincular_filial(id: int=0, id_filial:int=0, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    schema = sUsuarioFilialExclusao(**{'usuario':id, 'filial':id_filial})
    try:
        desvinculo = excluir_entidade(UsuarioFilial, schema, ator, sessao, ['usuario', 'filial'])
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return desvinculo

        
