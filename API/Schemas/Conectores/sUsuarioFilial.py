from API.Schemas.base import *

class sUsuarioFilialCriacao(BaseModel):
    usuario: int
    filial: int

class sUsuarioFilialExclusao(BaseModel):
    usuario: int
    filial: int