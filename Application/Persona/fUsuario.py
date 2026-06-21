
#Application
from Application.base import *

#API - Schemas
from API.Schemas.Persona.sUsuario import *

#Infrastructure
from Infrastructure.Repositories.Persona.reUsuario import *
from Infrastructure.Repositories.Persona.reCliente import *

from Domain.__exceptions__ import SchemaInvalido, AcessoInvalido

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def validar_schema_usuario_criar(schema: CriacaoSchema):
    if (not schema.nome) or (not schema.email) or (not schema.senha):
        raise SchemaInvalido(schema)

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def validar_schema_usuario_editar(schema: EdicaoSchema):
    if (not schema.nome) or (not schema.email) or (not schema.cargo):
        raise SchemaInvalido(schema)
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def validar_schema_usuario_logar(schema: LoginSchema):
    if not schema.email or not schema.senha:
        raise SchemaInvalido(schema)

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def autenticar_usuario(email: str, senha: str, sessao: Session):
    usuario = verificar_usuario_existe(sessao, email)
    if not bcrypt_context.verify(senha, usuario.senha):
        raise AcessoInvalido()
    return usuario

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def exec_busca(id, nome, email, cargo, ativo, filial, sessao: Session, usuario: Usuario, tipo=None):
    #Se tiver algum filtro, e o filtro não for validado, levanta NotFoundException
    lista = buscar_usuarios(id, nome, email, cargo, ativo, sessao, usuario, tipo)
    ator_na_lista = [item for item in lista if item['id'] == usuario.id]
    #Validação se o usuário é da mesma filial da qual a consulta realizada está sendo feita
    mesma_filial = True if filial in usuario.filiais else False
    if ator_na_lista != [] and usuario.cargo not in ['CEO', 'TI']:
        return ator_na_lista
    elif (cargo not in tipo or not mesma_filial) and usuario.cargo not in [Cargo.CEO, Cargo.TI]:
        raise SemPermissao(usuario, 'listar')
    return lista
