#Bases
from API.Routes.base import *
from Application.base import verificar_permissao, verificar_token
from Infrastructure.Repositories.base import Session, Depends, criar_sessao

from Domain.exceptions import PermissionExcept, ConflictExcept, SchemaInvalido, Conflito, SemPermissao, ExceptionHTTP, ExceptionGenerica

#Schema
from API.Schemas.Autenticacao.sCliente import *

#Application
from Application.Persona.fCliente import validar_schema_cliente_criar

#Repositories
from Infrastructure.Repositories.Persona.reCliente import criar_cliente_bd, verificar_cliente_criacao

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

cliente_router = APIRouter(prefix='/clientes', tags=['cliente'])

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


@cliente_router.post('/criar')
async def criar_cliente(schema: CriacaoSchema, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    '''
    Esta rota realiza a criação de um cliente no sistema

    ATENÇÃO! Utilizamos dados pessoais internamente em nosso sistema para a validação de promoções e asociações únicas.
    Seguem os usos internos de dados pessoais:
    - (obrigatório) CPF: associação de cliente único por CPF
    - Data de nascimento: Para filtros específicos de preferência de produto, com base na idade
    - Escaneamento facial: para facilitar o login no sistema
    - Encereço: para permitir entregas a domicílio de pedidos
    Se você quer que os dados opcionais sejam utilizados para lhe gerar uma experiência mais dinâmica do app, preencha-os.
    A criação de seu usuário demonstra consentimento sobre o uso dos dados inseridos em seu cadastro
    '''
    path = '/clientes/criar'
    try:
        validar_schema_cliente_criar(schema)
        verificar_permissao(ator, 'cliente', 'criar')
        verificar_cliente_criacao(schema.cpf, sessao)
        criacao = criar_cliente_bd(schema, sessao)
    except ExceptionHTTP:
        raise 
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return criacao

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

@cliente_router.get('/')
async def listar_clientes():
    pass

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

@cliente_router.put('/{id}')
async def atualizar_cliente(id: int, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    path = f'/clientes/{str(id)}'

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Ativar
@cliente_router.put('/{id}/ativar')
async def ativar_cliente(id: int):
    pass

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Desativar
@cliente_router.put('/{id}/desativar')
async def desativar_cliente(id: int):
    pass


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Atualizar fidelidade
@cliente_router.put('/{id}/fidelidade')
async def atualizar_fidelidade(id: int):
    pass

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Solicitar Reset Senha
@cliente_router.post('/{id}/reset')
async def resetar_senha(id: int):
    pass

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Autenticar
@cliente_router.post('/login')
async def login(schema, sessao):
    pass

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Desautenticar
@cliente_router.post('/logout')
async def logout():
    pass

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Atualizar Token
@cliente_router.post('/refresh')
async def refresh_token():
    pass
    #Pega o refresh_token e entrega um token normal