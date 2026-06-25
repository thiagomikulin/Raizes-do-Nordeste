from API.Schemas.base import *

class CriacaoSchema(BaseModel):
    filial: int
    #itens: Relationship
    ativo: bool

class ItemCriacaoSchema(BaseModel):
    ingrediente: int
    unidade_medida: str

class InternoItemCriacaoSchema(BaseModel):
    estoque: int
    ingrediente: int
    unidade_medida: str

class ItemEdicaoSchema(BaseModel):
    quantidade: int