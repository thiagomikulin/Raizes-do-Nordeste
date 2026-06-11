from Application.base import *

from API.Schemas.sCliente import *

def validar_schema_cliente_criar(schema: CriacaoSchema):
    #Aqui, delimita-se os campos necessários para validação do cliente
    '''
    Não obrigatório:
    * scanFace (no momento, em implementação futura, poderá ser)
    * endereco (no entanto, deve impedir encomenda se não tiver)
    * data_nasc
    '''
    if (not schema.nome) or (not schema.email) or (not schema.cpf) or (not schema.senha):
        raise SchemaExcept

def validar_schema_cliente_logar(schema: LoginSchema):
    if (not schema.email or not schema.cpf) or not schema.senha:
        raise SchemaExcept
