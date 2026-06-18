from API.Schemas.Itens.sIngredientes import CriacaoSchema

from Domain.exceptions import SchemaInvalido

def verificar_schema_criacao_ingrediente(schema: CriacaoSchema):
    if not schema.nome or not schema.periodo:
        raise SchemaInvalido(schema)