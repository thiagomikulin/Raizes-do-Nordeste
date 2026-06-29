from API.Schemas.base import *
from Domain.__exceptions__ import CamposObrigatorios
from Infrastructure.Models.Vendas.mPedido import StatusPagamento, TiposPed, CanalPedido, FormaPagamento

class CriacaoSchema(BaseModel):
  filial: int = Field(ge=1)
  #status: str
  tipoPedido: TiposPed
  canalPedido: CanalPedido
  #tipo_criador: str 
  #id_criador: int #(NÃO É OPCIONAL, MUDAR DIAGRAMA)
  cliente: Optional[int] #Opcional
  #tipo_modificador: str
  #id_modificador: int #Na criação, será o mesmo que o id_criador
  #data: date
  mesa: Optional[int]
  chamada: Optional[int]
  endereco: Optional[str]
  forma_pagamento: FormaPagamento
  #soma_itens: float
  #frete: float
  #total: float
  #pontos_fidelidade_desconto: int

  class Config:
    from_attributes=True

  @model_validator(mode='after')
  def verificar_tipo_pedido(self):
    mesa = self.mesa
    chamada = self.chamada
    endereco = self.endereco
    cliente = self.cliente
    tipoPedido = self.tipoPedido

    if mesa == "" and tipoPedido == TiposPed.MESA:
      raise CamposObrigatorios({'mesa':mesa, 'tipo_pedido':tipoPedido.value})
    elif chamada == "" and tipoPedido == TiposPed.BALCAO:
      raise CamposObrigatorios({'chamada':chamada, 'tipo_pedido':tipoPedido.value})
    elif endereco == "" and tipoPedido == TiposPed.ENTREGA:
      raise CamposObrigatorios({'endereco':endereco, 'tipo_pedido':tipoPedido.value})
    elif cliente == "" and (mesa == '' and chamada == ''):
      raise CamposObrigatorios({'cliente':cliente, 'mesa':mesa, 'chamada':chamada})
    return self



class EdicaoSchema(BaseModel):
  tipo: str
  cliente: Optional[int] #Opcional
  mesa: Optional[int]
  chamada: Optional[int]
  endereco: Optional[str]
  forma_pagamento: FormaPagamento
  desconto_fidelidade: int

