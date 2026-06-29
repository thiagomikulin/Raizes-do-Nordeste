
from Domain.__exceptions__ import ExceptionRequest, FalhaNaSolicitacao
import requests

def mock_solicitar_pagamento(conta: str, cpf:str, valor: float):
    corpo = {
        "conta":conta,
        "cpf":cpf,
        "valor":valor
    }
    retorno = requests.post('http://mock:5000/pagamentos/solicitar', json=corpo)
    print(retorno.status_code)
    print(retorno.json())
    if retorno.status_code != 200:
        raise FalhaNaSolicitacao()
    return retorno.json()
    
def mock_consultar_pagamento(id):
    if id is None:
        return
    parametro = {
        "id":id
    }
    retorno = requests.get('http://mock:5000/pagamentos/', params=parametro)
    print(retorno.status_code)
    if retorno.status_code != 200:
        raise FalhaNaSolicitacao()
    else:
        return retorno.json()
    
def mock_cancelar_pagamento(id):
    retorno = requests.patch(f'http://mock:5000/pagamentos/{id}/cancelar')
    print(retorno)
    if retorno.status_code != 200:
        raise FalhaNaSolicitacao()
    else:
        return retorno.json()
