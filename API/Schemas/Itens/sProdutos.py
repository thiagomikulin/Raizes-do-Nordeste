from API.Schemas.base import *

class CriacaoSchema(BaseModel):
  nome: str
  # variacoes: relationship
  #ativo: bool

class EdicaoSchema(BaseModel):
  nome: str