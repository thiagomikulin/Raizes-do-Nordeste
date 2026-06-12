from API.Schemas.base import *

class StatusPedido(str,Enum):
    ABERTO = "Aberto"

class CriacaoSchema(BaseModel):
  filial: int
  status: StatusPedido
  #tipoPedido: ENUM
  #canalPedido: ENUM
  #tipo_criador: ENUM 
  id_criador: int #(NÃO É OPCIONAL, MUDAR DIAGRAMA)
  cliente: Optional[int] #Opcional
  #tipo_modificador: ENUM
  id_modificador: int #Na criação, será o mesmo que o id_criador
  #data: date
  mesa: Optional[int]
  #itens: relationship
  chamada: Optional[int]
  endereco: Optional[int]
  soma_itens: float
  frete: float
  total: float
  pontos_fidelidade_desconto: int
