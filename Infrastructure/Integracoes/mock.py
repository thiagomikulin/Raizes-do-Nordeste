
from Domain.__exceptions__ import ExceptionRequest, FalhaNaSolicitacao
import requests

def mock_solicitar_pagamento(conta: str, cpf:str, valor: float):
    corpo = {
        "conta":conta,
        "cpf":cpf,
        "valor":valor
    }
    retorno = requests.post('0.0.0.0:5000/pagamentos/solicitar', corpo)
    if retorno.status_code != 200:
        raise FalhaNaSolicitacao()
    
def mock_consultar_pagamento(id):
    corpo = {'id':id}
    retorno = requests.get('0.0.0.0:5000/pagamentos/', corpo)
    if retorno.status_code != 200:
        raise FalhaNaSolicitacao
    else:
        return retorno
