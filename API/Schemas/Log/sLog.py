from API.Schemas.base import *

class CriacaoSchema(BaseModel):
  acao: str
  tabela: str
  campo: str
  valor_ant: str
  valor_novo: str
  # tipo_pessoa: ENUM
  id_pessoa: int
  #data: date
  #hora: time
