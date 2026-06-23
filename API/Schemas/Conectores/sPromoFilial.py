from API.Schemas.base import *

class sPromoFilialCriacao(BaseModel):
    promocao: int
    filial: int

class sPromoFilialExclusao(BaseModel):
    promocao: int
    filial: int