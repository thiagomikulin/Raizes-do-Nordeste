from Infrastructure.Repositories.base import Session, Depends, criar_sessao

#Requisitos
from API.Schemas.Empresa.sCampanhaPromo import CriacaoSchema

def verificar_campanha_existe(id: int, sessao: Session):
    campanha = 'campanha'
    return campanha

def criar_campanha_bd(schema: CriacaoSchema, sessao: Session):
    campanha = 'campanha'
    return campanha

def editar_campanha_bd():
    pass

def ativar_campanhapromo_bd():
    pass

def desativar_campanhapromo_bd():
    pass
