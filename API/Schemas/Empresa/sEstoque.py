from API.Schemas.base import *

class CriacaoSchema(BaseModel):
    filial: int
    #itens: Relationship
    ativo: bool

class ItemCriacaoSchema(BaseModel):
    pass

class ItemEdicaoSchema(BaseModel):
    pass