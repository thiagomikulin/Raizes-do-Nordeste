from Application.base import *

from Domain.exceptions import SchemaInvalido, AcessoInvalido

from API.Schemas.Autenticacao.sCliente import LoginSchema, CriacaoSchema
from Infrastructure.Repositories.Persona.reCliente import verificar_cliente_existe, bcrypt_context

def validar_schema_cliente_criar(schema: CriacaoSchema):
    #Aqui, delimita-se os campos necessários para validação do cliente
    '''
    Não obrigatório:
    * scanFace (no momento, em implementação futura, poderá ser)
    * endereco (no entanto, deve impedir encomenda se não tiver)
    * data_nasc
    '''
    if (not schema.nome) or (not schema.email) or (not schema.cpf) or (not schema.senha):
        raise SchemaInvalido(schema)

def validar_schema_cliente_logar(schema: LoginSchema):
    if (not schema.email and not schema.cpf) or not schema.senha:
        raise SchemaInvalido(schema)

def autenticar_cliente(schema: LoginSchema, sessao: Session):
    cliente = verificar_cliente_existe(sessao, email=schema.email if schema.email else None, cpf=schema.cpf if schema.cpf else None)
    if not bcrypt_context.verify(schema.senha, cliente.senha):
        raise AcessoInvalido()
    return cliente

def atualizar_fidelidade_valida(id: int, fidelidade: int, sessao: Session):
    if fidelidade < 0:
        raise 
