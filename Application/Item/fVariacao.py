from API.Schemas.Itens.sVariacoes import CriacaoSchema

def verificar_schema_criacao_variacao(schema: CriacaoSchema):
    if not schema.nome or not schema.produto or not schema.preco_unitario:
        