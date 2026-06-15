#Bases
from API.Routes.base import *
from Application.base import verificar_permissao, verificar_token
from Infrastructure.Repositories.base import Session, Depends, criar_sessao

from Domain.exceptions import SchemaExcept, PermissionExcept, ConflictExcept, SchemaInvalido, Conflito, SemPermissao

#Schema
from API.Schemas.Autenticacao.sCliente import *

#Application
from Application.fCliente import validar_schema_cliente_criar

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
    except SchemaExcept:
        raise SchemaInvalido(schema, path)
    except PermissionExcept:
        raise SemPermissao(path, ator)
    except ConflictExcept:
        raise Conflito(entidade='cliente', campo='cpf', valor_campo=schema.cpf, path=path)
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

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Desativar

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Atualizar fidelidade

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Solicitar Reset Senha

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Autenticar

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Desautenticar

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Atualizar Token