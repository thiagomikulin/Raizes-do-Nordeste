from API.Schemas.Empresa.sCampanhaPromo import *

class CriacaoSchema(BaseModel):
    nome: str
    desconto: int
    #validade: date
    ativo: bool