#Bases
from API.Routes.base import *
from Application.base import criar_token, verificar_permissao, verificar_token, timedelta
from Infrastructure.Repositories.base import Session, Depends, criar_sessao

from Application.chamada_rota import ativar_entidade, atualizar_campo, criar_entidade, desativar_entidade, editar_entidade, visualizar_entidade

#Exceptions
from Domain.__exceptions__ import PermissionExcept, ConflictExcept, SchemaInvalido, Conflito, SemPermissao, ExceptionHTTP, ExceptionGenerica
#Logs
from Infrastructure.Repositories.Registros.reLogs import salvar_log_bd

#Requisitos
from API.Schemas.Persona.sCliente import *
from Application.Persona.fCliente import validar_schema_cliente_criar, validar_schema_cliente_logar, autenticar_cliente, atualizar_fidelidade_valida
from Infrastructure.Repositories.Persona.reCliente import criar_cliente_bd, verificar_cliente_criacao, verificar_cliente_existe, desativar_cliente_bd, ativar_cliente_bd
from Infrastructure.Models.Persona.mCliente import Cliente

#Complementares
from Infrastructure.Integracoes.email import solicitar_reset_senha

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

cliente_router = APIRouter(prefix='/clientes', tags=['Persona - Cliente'])

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Clientes - Criar (RF-C01)
@cliente_router.post('/criar')
async def criar_cliente(schema: CriacaoSchema, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    '''
    Esta rota realiza a criação de um cliente no sistema

    ATENÇÃO! Utilizamos dados pessoais internamente em nosso sistema para a validação de promoções e asociações únicas.
    Seguem os usos internos de dados pessoais:
    - (obrigatório) CPF: associação de cliente único por CPF
    - Data de nascimento: Para filtros específicos de preferência de produto, com base na idade
    - Escaneamento facial: para facilitar o login no sistema
    - Endereço: para permitir entregas a domicílio de pedidos
    
    Se você quer que os dados opcionais sejam utilizados para lhe gerar uma experiência mais dinâmica do app, preencha-os.
    A criação de seu usuário demonstra consentimento sobre o uso dos dados inseridos em seu cadastro
    '''
    try:
        cliente = criar_entidade(
            Cliente, 
            schema, 
            ator, 
            sessao, 
            campo_verificacao=['cpf', 'email'],
            lista_regras_validacao=[], 
            lista_regras_pos = []
        )
    except ExceptionHTTP:
        raise 
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return cliente

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Clientes - Visualizar (RF-C02)
@cliente_router.get('/')
async def listar_clientes(
    id: int | None = None,
    nome: str | None=  None,
    email: str | None = None,
    cpf: str | None = None,
    fidelidade: int | None = None,
    data_nasc: date | None = None,
    ativo: bool | None=True,
    sessao: Session = Depends(criar_sessao), 
    ator=Depends(verificar_token)
    ):
    dict_campos = {
        "id":id,
        'nome':nome,
        'email':email,
        'cpf':cpf,
        'fidelidade':fidelidade,
        'data_nasc':data_nasc,
        'ativo':ativo
    }
    try:
        lista = visualizar_entidade(Cliente, sessao, ator, dict_campos)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    return lista

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Clientes - Editar (RF-C03)
@cliente_router.put('/{id}')
async def atualizar_cliente(id: int, schema: EdicaoSchema, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        edicao = editar_entidade(id, Cliente,schema, ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    return edicao

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Clientes - Ativar (RF-C04)
@cliente_router.put('/{id}/ativar')
async def ativar_cliente(id: int, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        ativado = ativar_entidade(Cliente, ator, id, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return ativado

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Clientes - Desativar (RF-C04)
@cliente_router.put('/{id}/desativar')
async def desativar_cliente(id: int, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        desativado = desativar_entidade(Cliente, ator, id, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return desativado


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Clientes - Atualizar fidelidade (RF-C05)
@cliente_router.put('/{id}/fidelidade')
async def atualizar_fidelidade(id: int, fidelidade: int, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        fidelidade = atualizar_campo(Cliente, id, 'fidelidade', fidelidade, ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    return fidelidade


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Clientes - Solicitar Reset Senha (RF-C06)
@cliente_router.post('/reset_senha')
async def reset_senha(email: str, sessao: Session = Depends(criar_sessao)):
    try:
        verificar_cliente_existe(email=email, sessao=sessao)
        reset = solicitar_reset_senha(email)
        #Recebe o usuário autenticado e envia um request de troca de senha para o email
        #Se não tiver email cadastrado, retorna erro e indica para contatar equipe técnica
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return reset


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Clientes - Autenticar (RF-C07)
@cliente_router.post('/login')
async def login(schema: LoginSchema, sessao: Session=Depends(criar_sessao)):
    try:
        validar_schema_cliente_logar(schema)
        cliente = autenticar_cliente(schema, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        access_token = criar_token(cliente.id, Cliente)
        refresh_token = criar_token(cliente.id, Cliente, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token":refresh_token,
            "token_type":"Bearer"
        }

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Cliente - Atualizar Token (RF-C08)
@cliente_router.post('/refresh')
async def refresh_token(ator=Depends(verificar_token)):
    ac = criar_token(ator.id)
    return {
        "access_token":ac,
        "token_type":"Bearer"
    }
    #Pega o refresh_token e entrega um token normal