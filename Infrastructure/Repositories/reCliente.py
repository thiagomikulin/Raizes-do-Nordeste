
from API.Schemas.Autenticacao.sCliente import *

from Infrastructure.Repositories.base import Session
from Infrastructure.Models.Persona.mCliente import *

from Domain.exceptions import ConflictExcept

def verificar_cliente_criacao(email, sessao:Session):
    cliente = sessao.query(Cliente).filter(Cliente.email == email).first()
    if cliente:
        raise ConflictExcept
    return cliente
