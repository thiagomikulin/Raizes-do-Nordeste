from API.Schemas.base import *

class CriacaoSchema(BaseModel):
    cidade: str
    endereco: str
    # estoque: int (Criado automaticamente)
    conta_banc: str
    # campanha_promo: Relationship

class EdicaoSchema(BaseModel):
    pass