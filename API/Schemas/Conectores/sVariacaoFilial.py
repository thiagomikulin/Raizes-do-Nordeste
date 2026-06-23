from API.Schemas.base import *

class sVariacaoFilialCriacao(BaseModel):
    variacao: int
    filial: int

class sVariacaoFilialExclusao(BaseModel):
    variacao: int
    filial: int