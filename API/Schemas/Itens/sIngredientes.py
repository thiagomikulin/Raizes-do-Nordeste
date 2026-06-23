from API.Schemas.base import *

from Infrastructure.Models.Item.mIngrediente import PeriodoAno

class CriacaoSchema(BaseModel):
  nome: str
  periodo: PeriodoAno

class EdicaoSchema(BaseModel):
  nome: str
  periodo: PeriodoAno