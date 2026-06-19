from Infrastructure.Repositories.base import Session, Depends, criar_sessao
from Infrastructure.Models.Empresa.mEstoque import Estoque

def criar_estoque_bd(id_filial, sessao: Session = Depends(criar_sessao)):
    novo_estoque = Estoque(id_filial)
    sessao.add(novo_estoque)
    sessao.commit()
    return novo_estoque.id

def verificar_estoque_existe():
    pass
