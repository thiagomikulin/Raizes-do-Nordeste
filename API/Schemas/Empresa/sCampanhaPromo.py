from pydantic import BaseModel

class CriacaoSchema(BaseModel):
    nome: str
    desconto: int
    #validade: date
    ativo: bool