
from API.Schemas.sCliente import *

from Infrastructure.Repositories.base import *
from Infrastructure.Models.Persona.mCliente import *

def verificar_cliente_criacao(email, sessao:Session):
    cliente = sessao.query(Cliente).filter(Cliente.email == email).first()
    if cliente:
        raise ConflictExcept
    return cliente
