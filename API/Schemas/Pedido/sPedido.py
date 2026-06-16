from API.Schemas.base import *

class CriacaoSchema(BaseModel):
  filial: int
  #status: str
  tipoPedido: str
  canalPedido: str
  #tipo_criador: str 
  #id_criador: int #(NÃO É OPCIONAL, MUDAR DIAGRAMA)
  cliente: Optional[int] #Opcional
  #tipo_modificador: str
  #id_modificador: int #Na criação, será o mesmo que o id_criador
  #data: date
  mesa: Optional[int]
  chamada: Optional[int]
  endereco: Optional[str]
  forma_pagamento: str
  #soma_itens: float
  #frete: float
  #total: float
  #pontos_fidelidade_desconto: int
