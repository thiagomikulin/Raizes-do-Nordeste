from API.Schemas.base import *

class CriacaoSchema(BaseModel):
    # data: date
    # status: enum
    filial: int
    # tipo_mov: enum
    # itens: Relationship
    # validade: date
    chave_nota: str