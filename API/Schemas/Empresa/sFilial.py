from API.Schemas.base import *

class CriacaoSchema(BaseModel):
    cidade: str
    # estrutura: Enum
    endereco: str
    ativo: bool
    estoque: int
    conta_banc: str
    # campanha_promo: Relationship