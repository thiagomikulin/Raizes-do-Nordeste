

from main import db, sessionmaker, Session, bcrypt_context

from Application.base import *

from Infrastructure.Models.base import EnumPy

from Domain.__exceptions__ import Conflito, NaoEncontrado

async def criar_sessao():
    #verificação de existência de usuários
    try:
        Session = sessionmaker(bind=db)
        sessao = Session() #Criação de sessão (cursor)
        yield sessao
    finally:
        sessao.close()

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def verificar_entidade_criacao(entidade, schema, nome_entidade, campos: list, sessao: Session):
    if campos is None:
        return
    else:
        for campo in campos:
            coluna = getattr(entidade, campo)
            entidade = sessao.query(entidade).filter(coluna == getattr(schema, campo)).first()
    
    if entidade:
        raise Conflito(nome_entidade, campo, getattr(schema, campo))

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def verificar_subentidade_criacao(entidade, id_esq, id_dir, sessao:Session):
    existe = sessao.query(entidade).filter()

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def criar_entidade_bd(entidade, schema, sessao):
    schema_dump = schema.model_dump()
    if "senha" in schema_dump:
        schema_dump['senha'] = bcrypt_context.hash(schema_dump["senha"])
    if "conta_banc" in schema_dump:
        schema_dump['conta_banc'] = bcrypt_context.hash(schema_dump["conta_banc"])
    nova_entidade = entidade(**schema_dump)
    sessao.add(nova_entidade)
    sessao.commit()
    return {
        'message':f"{entidade.__name__} {nova_entidade.id} criado com sucesso!",
        f"{entidade.__name__}":{chave:valor for chave, valor in nova_entidade.__dict__.items() if chave not in ['senha', 'cpf', 'conta_banc']} 
        
    }

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def exec_busca(entidade, dict_campos: dict, sessao):
    busca = sessao.query(entidade)

    #Filtro
    for chave, valor in dict_campos.items():
        if valor is None:
            continue
        coluna = getattr(entidade, chave)
        if type(valor) == str:
            busca = busca.filter(coluna.contains(valor))
        elif isinstance(valor, bool) or isinstance(valor, EnumPy) or isinstance(valor, int):
            busca = busca.filter(coluna == valor)


    #Retorno de tudo
    retorno = busca.all()

    #Filtro de exibição de campos não permitidos (dá pra otimizar, mas leva dessa forma por ora mesmo pelo prazo)
    lista = []
    for itens in retorno:
        item = {}
        for chave, valor in itens.__dict__.items():
            if chave in ['senha', 'cpf', 'scanFace', 'conta_banc']: #Dados sensíveis
                continue
            else:
                item[chave] = valor
        lista.append(item)
    

    if not lista:
        raise NaoEncontrado(dict_campos)
    return lista

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def verificar_entidade_existe(entidade, id, sessao:Session):
    check = sessao.query(entidade).filter(entidade.id == id).first()
    if not check:
        raise NaoEncontrado({"id":id})
    return check

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def editar_entidade_bd(schema, nome_entidade, entidade, campos, sessao:Session):
    schema_dump = schema.model_dump()
    for campo in campos:
        setattr(entidade, campo, schema_dump[campo])
    sessao.commit()
    return {
        "message":f"{nome_entidade} {entidade.id} atualizado com sucesso!",
        f"{nome_entidade}":{chave:valor for chave, valor in entidade.__dict__.items() if chave not in ['senha', 'cpf', 'conta_banc']}
    }

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def ativar_entidade_bd(entidade, nome_entidade, sessao):
    if entidade.ativo == True:
        raise NaoAlterado(entidade)
    entidade.ativo = True
    sessao.commit()
    return {
        "message":f'{nome_entidade} {entidade.id} ativado com sucesso!',
        f'{nome_entidade}':{chave:valor for chave, valor in entidade.__dict__.items() if chave not in ['senha', 'cpf', 'conta_banc']}
    }

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def desativar_entidade_bd(entidade, nome_entidade, sessao):
    if entidade.ativo == False:
        raise NaoAlterado(entidade)
    entidade.ativo = False
    sessao.commit()
    return {
        "message":f'{nome_entidade} {entidade.id} desativado com sucesso!',
        f'{nome_entidade}':{chave:valor for chave, valor in entidade.__dict__.items() if chave not in ['senha', 'cpf', 'conta_banc']}
    }

