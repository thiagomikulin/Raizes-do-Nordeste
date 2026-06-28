from main import bcrypt_context

from API.Schemas.Persona.sCliente import *

from Infrastructure.Repositories.base import Session
from Infrastructure.Models.Persona.mCliente import *

from Domain.__exceptions__ import Conflito, NaoEncontrado, NaoAlterado

def verificar_cliente_criacao(cpf, sessao:Session):
    cliente = sessao.query(Cliente).filter(Cliente.cpf == cpf).first()
    if cliente:
        raise Conflito('cliente', 'cpf', cpf)
    return cliente

def cliente_existe(id, sessao: Session):
    if id:
        cliente = sessao.query(Cliente).filter(Cliente.id == id).first()
        if not cliente:
            raise NaoEncontrado(campos={'id':id})
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
        "cliente":{
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

def verificar_cliente_existe(sessao: Session, email=None, id=None, cpf=None):
    if email:
        cliente = sessao.query(Cliente).filter(Cliente.email == email).first()
    elif id:
        cliente = sessao.query(Cliente).filter(Cliente.id == id).first()
    elif cpf:
        cliente = sessao.query(Cliente).filter(Cliente.cpf == cpf).first()
    else:
        raise
    if not cliente:
        raise NaoEncontrado(campos={'email':email, "id":id, "cpf":cpf})
    return cliente

def desativar_cliente_bd(cliente: Cliente, sessao: Session):
    if cliente.ativo == False:
        raise NaoAlterado(cliente,  {'ativo':cliente.ativo})
    cliente.ativo = False
    sessao.commit()
    return {
        "message": "Cliente desativado com sucesso!",
        "cliente":{
            "id":cliente.id,
            "nome":cliente.nome,
            "ativo": cliente.ativo
        }
    }

def ativar_cliente_bd(cliente: Cliente, sessao:Session):
    if cliente.ativo == True:
        raise NaoAlterado(cliente, {'ativo':cliente.ativo})
    cliente.ativo = True
    sessao.commit()
    return {
        "message": "Cliente ativado com sucesso!",
        "cliente":{
            "id":cliente.id,
            "nome":cliente.nome,
            "ativo": cliente.ativo
        }
    }