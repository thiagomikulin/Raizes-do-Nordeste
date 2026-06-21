from API.Schemas.Itens.sVariacoes import CriacaoSchema

from Domain.__exceptions__ import SchemaInvalido

def verificar_schema_criacao_variacao(schema: CriacaoSchema):
    if not schema.nome or not schema.produto or not schema.preco_unitario:
        raise SchemaInvalido(schema)