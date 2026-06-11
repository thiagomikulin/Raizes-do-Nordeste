from API.Schemas.base import *

class CriacaoSchema(BaseModel):
  nome: str
  # periodo: enum
  ativo: bool
