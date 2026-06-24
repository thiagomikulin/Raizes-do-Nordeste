from API.Schemas.base import *

class CriacaoSchema(BaseModel):
    nome: str
    desconto: int
    validade: date
    #ativo: bool

class EdicaoSchema(BaseModel):
    nome: str
    desconto: int
    validade: date