from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from enum import Enum

# A ideia por traz dessa ""implementação"" de mock de pagamento seria como uma solicitação de pix, gerada e direcionada a um CPF específico 

app = FastAPI(
    title='Mock API',
    description='API para pagamentos mock, apenas para teste da Raízes do Nordeste'
)

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class StatusPagamento(str, Enum):
    SOLICITADO = 'Solicitado'
    ESTORNADO = 'Estornado'
    CANCELADO = 'Cancelado'
    APROVADO = 'Aprovado'

class PagamentoMock():

    id = 0

    #A inicialização contaria como a solicitação do pagamento
    def __init__(self, conta, cpf, valor):
        self.conta = conta
        self.cpf = cpf
        self.status = StatusPagamento.SOLICITADO
        self.valor = valor
        PagamentoMock.id += 1
        self.id = PagamentoMock.id

    def estornarPagamento(self):
        self.status = StatusPagamento.ESTORNADO

    def cancelarPagamento(self):
        self.status = StatusPagamento.CANCELADO

    def aprovarPagamento(self):
        self.status = StatusPagamento.APROVADO



#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
pagamentos = {}

class SolicitarPagamento(BaseModel):
    conta: str
    cpf: str
    valor: float

    class Config:
        from_attributes=True

@app.post('/pagamentos/solicitar', status_code=200)
async def solicitar_pagamento(schema: SolicitarPagamento):
    pagamento = PagamentoMock(schema.conta, schema.cpf, schema.valor)
    pagamentos[pagamento.id] = pagamento
    return {
        "message":"Pagamento solicitado!",
        "pagamento":{
            "id":pagamento.id,
            "status":pagamento.status
        }
    }

@app.patch('/pagamentos/{id}/estornar')
async def estornar_pagamento(id: int):
    pagamento = pagamentos.get(id)
    if pagamento is None:
        raise HTTPException(status_code=404, detail='Pagamento não encontrado')
    pagamentos[id].estornarPagamento()

@app.patch('/pagamentos/{id}/cancelar')
async def cancelar_pagamento(id:int):
    pagamento = pagamentos.get(id)
    if pagamento is None:
        raise HTTPException(status_code=404, detail='Pagamento não encontrado')

    pagamentos[id].cancelarPagamento()

@app.patch('/pagamentos/{id}/aprovar')
async def aprovar_pagamento(id: int):
    pagamento = pagamentos.get(id)
    if pagamento is None:
        raise HTTPException(status_code=404, detail='Pagamento não encontrado')

    pagamentos[id].aprovarPagamento()



@app.get('/pagamentos')
async def consultar_pagamento(
    id: int | None=None
):
    pagamento = pagamentos.get(id)
    if pagamento is None:
        raise HTTPException(status_code=404, detail='Pagamento não encontrado')
    return pagamentos[id]

    
