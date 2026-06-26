

from enum import Enum

from main import db, sessionmaker, Session, bcrypt_context, fernet

from Application.base import *

from Infrastructure.Models.base import EnumPy, inspect

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

def verificar_entidade(entidade, schema, nome_entidade, campos: list, sessao: Session, acao):
    if campos is None:
        return
    else:
        contador = 0
        for campo in campos:
            coluna = getattr(entidade, campo)
            busca = sessao.query(entidade).filter(coluna == getattr(schema, campo)).first()
            if busca:
                contador += 1
        if acao == 'criar':
            if contador == len(campos):
                encontrados = {f'{campo}':f'{getattr(schema, campo)}' for campo in campos}
                raise Conflito(nome_entidade, encontrados)
        elif acao == 'excluir':
            if contador < len(campos):
                raise NaoEncontrado(campos)
            

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def criar_entidade_bd(entidade, schema, sessao, ator, chaves=['id']):
    schema_dump = schema.model_dump()
    if entidade.__name__ == 'Pedido':
        schema_dump['tipo_criador'] = f'{ator.__class__.__name__}'
        schema_dump['id_criador'] = ator.id
    if "senha" in schema_dump:
        schema_dump['senha'] = bcrypt_context.hash(schema_dump["senha"])
    if "conta_banc" in schema_dump:
        valor = fernet.encrypt(schema_dump["conta_banc"].encode('utf-8'))
        print(len(valor))
        schema_dump['conta_banc'] = valor
    nova_entidade = entidade(**schema_dump)
    sessao.add(nova_entidade)
    sessao.commit()
    sessao.refresh(nova_entidade)
    dados_entidade = {chave:valor for chave, valor in nova_entidade.__dict__.items() if chave not in ['senha', 'cpf', 'conta_banc']} 
    campos = [f'{chave} = {valor}' for chave, valor in schema_dump.items() if chave not in ['senha', 'cpf', 'conta_banc']]
    retorno = ''
    if len(campos) > 1 :
        for campo in range(len(chaves)):
            retorno += f' e {campos[campo]}' if campo > 0 else f'{campos[campo]}'
    else:
        retorno = campos[0]
    return {
        'message':f"{entidade.__name__} {retorno} criado com sucesso!",
        f"{entidade.__name__}":dados_entidade 
        
    }

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def excluir_entidade_bd(entidade, schema, sessao:Session):
    schema_dump = schema.model_dump()
    busca = sessao.query(entidade)
        #Filtro
    for chave, valor in schema_dump.items():
        if valor is None:
            continue
        coluna = getattr(entidade, chave)
        if type(valor) == str:
            busca = busca.filter(coluna.contains(valor))
        elif isinstance(valor, (bool, EnumPy,  int)):
            busca = busca.filter(coluna == valor)

    #Retorno de tudo
    retorno = busca.first()
    dados_excluido = {chave:valor for chave, valor in retorno.__dict__.items()}
    campos = [f'{chave} = {valor}' for chave, valor in schema_dump.items()]
    if len(campos) > 1:
        mensagem = ' e '.join(campos)
    else:
        mensagem = campos[0]
    sessao.delete(retorno)
    sessao.commit()
    return {
        "message":f"O {entidade.__name__} com {mensagem} foi excluído com sucesso!",
        f"{entidade.__name__}":dados_excluido
    }

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def exec_busca(entidade, dict_campos: dict, sessao, permissoes):
    busca = sessao.query(entidade)

    #Filtro
    for chave, valor in dict_campos.items():
        if valor is None:
            continue
        coluna = getattr(entidade, chave)
        if type(valor) == str:
            busca = busca.filter(coluna.contains(valor))
        elif isinstance(valor, (bool, EnumPy,  int)):
            busca = busca.filter(coluna == valor)

    #Retorno de tudo
    retorno = busca.all()

    if entidade.__name__ == 'Usuario':
        tipo = 'Usuario'
    else:
        tipo = ''

    #Filtro de exibição de campos não permitidos (dá pra otimizar, mas leva dessa forma por ora mesmo pelo prazo)
    lista = []
    for itens in retorno:
        item = {}

        mapa_campos = inspect(itens)
        for coluna in mapa_campos.mapper.column_attrs:
            nome = coluna.key

            #Campos normais
            if nome in ['senha', 'cpf', 'scanFace', 'conta_banc']: #Dados sensíveis
                continue

            item[nome] = getattr(itens, nome)
            


        #Relationship
        for relacao in mapa_campos.mapper.relationships:
            nome = relacao.key

            item[nome] = getattr(itens, nome)

        #Controle de permissão de view de usuário
        if tipo == 'Usuario':
            cargo = f'{tipo} - {item['cargo'].value}'
            if cargo in permissoes:
                lista.append(item)
        else:
            lista.append(item)
        

        # for chave, valor in itens.__dict__.items():
        #     if chave in ['senha', 'cpf', 'scanFace', 'conta_banc']: #Dados sensíveis
        #         continue
        #     else:
        #         item[chave] = valor
    

    if not lista:
        raise NaoEncontrado(dict_campos)
    return lista

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def verificar_entidade_existe(entidade, id, sessao:Session):
    if type(id) == dict:
        for chave, valor in id.items():
            coluna = getattr(entidade, chave)
            check = sessao.query(entidade).filter(coluna == valor).first()
        if not check:
            raise NaoEncontrado({chave, valor} for chave, valor in id.items())
    else:
        check = sessao.query(entidade).filter(entidade.id == id).first()
        if not check:
            raise NaoEncontrado({"id":id})
    return check

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def editar_entidade_bd(schema, nome_entidade, entidade, campos, sessao:Session, ator):
    schema_dump = schema.model_dump()
    if nome_entidade == 'Pedido':
        campos.append('tipo_modificador')
        schema_dump['tipo_modificador'] = f'{ator.__class__.__name__}'
        campos.append('id_modificador')
        schema_dump['id_modificador'] = str(ator.id)

    for campo in campos:
        setattr(entidade, campo, schema_dump[campo])
    sessao.commit()
    sessao.refresh(entidade)
    itens = list(entidade.__dict__.items())
    lista_str = []
    for chave, valor in itens:
        lista_str.append(f'{chave} - {valor}')
    lista_str.pop(0)
    if len(lista_str) > 1:
        mensagem = ' e '.join(lista_str)
    else:
        mensagem = lista_str[0]
    return {
        "message":f"O {nome_entidade} com {mensagem} foi atualizado com sucesso!",
        f"{nome_entidade}":{chave:valor.value if isinstance(valor, Enum) else valor for chave, valor in entidade.__dict__.items() if chave not in ['senha', 'cpf', 'conta_banc']}
    }

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def editar_campo_entidade_bd(entidade, campo, valor, nome_entidade, sessao: Session):
    setattr(entidade, campo, valor)
    sessao.commit()
    return {
        "message":f"O {nome_entidade} com id = {entidade.id} foi atualizado com sucesso!",
        f"{nome_entidade}":{campo:valor}
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

