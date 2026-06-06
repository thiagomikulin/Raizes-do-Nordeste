from fastapi import APIRouter

cliente_router = APIRouter(prefix='/cliente', tags=['cliente'])

@cliente_router.post('/criar')
async def criar_cliente():
    '''
    Esta rota realiza a criação de um cliente no sistema

    ATENÇÃO! Utilizamos dados pessoais internamente em nosso sistema para a validação de promoções e asociações únicas.
    Seguem os usos internos de dados pessoais:
    - CPF: associação de cliente único por CPF
    - Data de nascimento: Para filtros específicos de preferência de produto, com base na idade
    - Escaneamento facial: para facilitar o login no sistema
    Se você quer que estes dados sejam utilizados para lhe gerar uma experiência mais dinâmica do app, preencha-os.
    Caso não queria compartilhar alguma destas informações, pedimos que preencha ao menos o CPF, para divisão dos perfis de uso.
    A criação de seu usuário demonstra consentimento sobre o uso dos dados inseridos em seu cadastro
    '''
