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
    tipoMov: TipoMov
    validade: date
    chave_nota: str

class ItemCriacaoSchema(BaseModel):
    ingrediente: int
    quantidade: int
    validade: date

class InternoItemCriacaoSchema(BaseModel):
    ingrediente: int
    movimentacao: int
    quantidade: int
    validade: date

class ItemEdicaoSchema(BaseModel):
    quantidade: int
    validade: date

class ItemExclusaoSchema(BaseModel):
    movimentacao: int
    id: int