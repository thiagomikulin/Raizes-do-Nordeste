from API.Schemas.base import *

class CriacaoSchema(BaseModel):
  nome: str
  produto: int
  # filiais: relationship
  # ingredientes: relationship
  preco_unitario: float

class EdicaoSchema(BaseModel):
  nome: str
  preco_unitario: float