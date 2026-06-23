from API.Schemas.base import *

class ReceitaCriacaoSchema(BaseModel):
    quantidade: int
    unidade_medida: str

class InternoReceitaCriacaoSchema(BaseModel):
    ingrediente: int
    variacao: int
    quantidade: int
    unidade_medida: str


class ReceitaExclusaoSchema(BaseModel):
    ingrediente: int
    variacao: int
    
class ReceitaEdicaoSchema(BaseModel):
    quantidade: int
    unidade_medida: str

class InternoReceitaEdicaoSchema(BaseModel):
    ingrediente: int
    variacao: int
    quantidade: int
    unidade_medida: str