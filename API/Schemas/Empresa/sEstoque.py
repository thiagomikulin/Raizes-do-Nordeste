from API.Schemas.base import *

class CriacaoSchema(BaseModel):
    filial: int
    #itens: Relationship
    ativo: bool

class ItemCriacaoSchema(BaseModel):
    ingrediente: int

class InternoItemCriacaoSchema(BaseModel):
    estoque: int
    ingrediente: int

class ItemEdicaoSchema(BaseModel):
    quantidade: int