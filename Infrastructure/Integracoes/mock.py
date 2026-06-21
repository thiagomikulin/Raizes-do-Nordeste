
from Domain.__exceptions__ import ExceptionRequest
import requests

def mock_solicitar_pagamento(conta: str, cpf:str, valor: float):
    corpo = {
        "conta":conta,
        "cpf":cpf,
        "valor":valor
    }
    retorno = requests.post('0.0.0.0:5000/pagamento/solicitar', corpo)
    if retorno.status_code != 200:
        raise ExceptionRequest(retorno)
