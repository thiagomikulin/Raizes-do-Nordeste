from API.Schemas.base import *

class ItemCriacaoSchema(BaseModel):
  variacao: int
  quantidade: int

class ItemEdicaoSchema(BaseModel):
  variacao: int
  quantidade: int

class InternoItemEdicaoSchema(BaseModel):
  id: int
  variacao: int
  quantidade: int

class InternoItemCriacaoSchema(BaseModel):
  id_ped: int
  variacao: int
  quantidade: int

class ItemExclusaoSchema(BaseModel):
  id_ped: int
  id: int