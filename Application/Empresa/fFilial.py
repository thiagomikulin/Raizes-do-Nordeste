from API.Schemas.Empresa.sFilial import *
from Infrastructure.Models.Empresa.mFilial import Filial

from Domain.exceptions import SchemaInvalido, NaoAlterado

def verificar_schema_criacao(schema: CriacaoSchema):
    if not schema.cidade or not schema.estrutura or not schema.endereco or not schema.ativo or not schema.conta_banc:
        raise SchemaInvalido(schema)

def verificar_schema_edicao():
    pass

def exec_busca():
    pass

def verificar_alteracao(filial: Filial, schema:EdicaoSchema):
    campos = []
    if (filial.cidade != schema.cidade):
        campos.append('cidade')
    if(filial.estrutura != schema.estrutura):
        campos.append('estrutura')  
    if (filial.endereco != schema.endereco):
        campos.append('endereco')
    if (filial.conta_banc != schema.conta_banc):
        campos.append('conta_banc')
    if len(campos) == 0:
        raise NaoAlterado(filial)