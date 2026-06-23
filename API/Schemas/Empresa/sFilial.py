from API.Schemas.base import *
from Infrastructure.Models.Empresa.mFilial import Estrutura

class CriacaoSchema(BaseModel):
    cidade: str
    endereco: str
    # estoque: int (Criado automaticamente)
    conta_banc: str
    # campanha_promo: Relationship

class EdicaoSchema(BaseModel):
    estrutura: Estrutura
    endereco: str