from API.Schemas.base import *
from Infrastructure.Models.Registros.mMovimentos import TipoMov

class CriacaoSchema(BaseModel):
    # data: date
    # status: enum
    filial: int
    tipo_mov: TipoMov
    # itens: Relationship
    validade: date
    chave_nota: str

class EdicaoSchema(BaseModel):
    pass

class ItemCriacaoSchema(BaseModel):
    pass