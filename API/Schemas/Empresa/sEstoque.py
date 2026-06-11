from API.Schemas.base import *

class CriacaoSchema(BaseModel):
    filial: int
    #itens: Relationship
    ativo: bool