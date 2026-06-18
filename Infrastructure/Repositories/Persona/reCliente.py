from main import bcrypt_context

from API.Schemas.Autenticacao.sCliente import *

from Infrastructure.Repositories.base import Session
from Infrastructure.Models.Persona.mCliente import *

from Domain.exceptions import ConflictExcept, NotFoundExcept

def verificar_cliente_criacao(cpf, sessao:Session):
    cliente = sessao.query(Cliente).filter(Cliente.cpf == cpf).first()
    if cliente:
        raise ConflictExcept
    return cliente

def cliente_existe(id, sessao: Session):
    if id:
        cliente = sessao.query(Cliente).filter(Cliente.id == id).first()
        if not cliente:
            raise NotFoundExcept(campos=["id"])
        else:
            return
    else:
        return

def criar_cliente_bd(schema: CriacaoSchema, sessao: Session):
    senha_criptografada = bcrypt_context.hash(schema.senha)
    novo_cliente = Cliente(
        nome=schema.nome, 
        email=schema.email, 
        cpf=schema.cpf, 
        scanFace=schema.scanFace, 
        senha=senha_criptografada, 
        endereco=schema.endereco, 
        fidelidade=0, 
        data_nasc=schema.data_nasc, 
        ativo=True)
    sessao.add(novo_cliente)
    sessao.commit()
    return {
        'message': 'Usuário criado com sucesso!',
        "usuario":{
            "id": novo_cliente.id,
            "nome":novo_cliente.nome,
            "email":novo_cliente.email,
            "cpf":novo_cliente.cpf,
            "endereco":novo_cliente.endereco,
            "fidelidade":novo_cliente.fidelidade,
            "nascimento":novo_cliente.data_nasc,
            "ativo": novo_cliente.ativo
        }
    }