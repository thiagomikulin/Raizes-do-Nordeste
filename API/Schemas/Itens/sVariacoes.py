from API.Schemas.base import *

class CriacaoSchema(BaseModel):
  nome: str
  produto: int
  # filiais: relationship
  # ingredientes: relationship
  ativo: bool
