from API.Schemas.Empresa.sFilial import *

from Domain.exceptions import SchemaExcept

def verificar_schema_criacao(schema: CriacaoSchema):
    if not schema.cidade or not schema.estrutura or not schema.endereco or not schema.ativo or not schema.conta_banc:
        raise SchemaExcept