from main import bcrypt_context

from Infrastructure.Repositories.base import Session

from Infrastructure.Models.Empresa.mFilial import *

from API.Schemas.Empresa.sFilial import *

#Estoque para criação
from Infrastructure.Models.Empresa.mEstoque import Estoque

def verificar_filial_criacao(conta_banc: str, sessao: Session):
    filial_check = sessao.query(Filial).filter(Filial.conta_banc == conta_banc).first()
    if filial_check:
        return
    
def criar_filial_bd(schema: CriacaoSchema, sessao: Session):
    conta_banc_cripto = bcrypt_context.hash(schema.conta_banc)
    nova_filial = Filial(schema.cidade, schema.endereco, conta_banc_cripto)
    sessao.add(nova_filial)
    sessao.commit()
    estoque = Estoque(nova_filial.id)
    sessao.add(estoque)
    sessao.commit()
    return {
        "message":"Filial criada com sucesso!",
        "filial":{
            "id":nova_filial.id,
            "cidade":nova_filial.cidade,
            "estrutura":nova_filial.estrutura,
            "endereco":nova_filial.endereco,
            "ativo":nova_filial.ativo,
            "estoque":nova_filial.estoque,
        }
    }