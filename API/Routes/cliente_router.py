from fastapi import APIRouter

from API.Routes.base import *
from API.Schemas.sCliente import *

from Application.fCliente import *

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

cliente_router = APIRouter(prefix='/cliente', tags=['cliente'])

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
        criacao = criar_cliente_db(schema)
    except SchemaExcept:
        raise SchemaInvalido(schema, path)
    except PermissionExcept:
        raise SemPermissao(path)
    except ConflictExcept:
        raise Conflito(entidade='cliente', campo='cpf', valor_campo=schema.cpf, path=path)
    else:
        return 
