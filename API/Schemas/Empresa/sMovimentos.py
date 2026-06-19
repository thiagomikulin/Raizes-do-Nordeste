from API.Schemas.base import *

class CriacaoSchema(BaseModel):
    # data: date
    # status: enum
    filial: int
    tipo_mov: str
    # itens: Relationship
    validade: date
    chave_nota: str

class EdicaoSchema(BaseModel):
    pass