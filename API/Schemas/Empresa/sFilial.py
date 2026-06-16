from API.Schemas.base import *

class CriacaoSchema(BaseModel):
    cidade: str
    estrutura: str
    endereco: str
    ativo: bool
    # estoque: int (Criado automaticamente)
    conta_banc: str
    # campanha_promo: Relationship