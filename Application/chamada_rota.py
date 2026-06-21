from Application.base import verificar_permissao

from Infrastructure.Repositories.base import verificar_entidade_criacao, criar_entidade_bd, Session, exec_busca
#Logs
from Infrastructure.Repositories.Registros.reLogs import salvar_log_bd

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def criar_entidade(entidade, schema, ator, sessao: Session, campo_verificacao=None, lista_regras_validacao: list = None, lista_regras_pos:list=None):
    nome_entidade = entidade.__name__
    verificar_permissao(ator, 'criar',nome_entidade, tipo='Não Classificado' if nome_entidade == 'Usuario' else None) #colocar validação para cargo internamente
    verificar_entidade_criacao(entidade, campo_verificacao, schema, nome_entidade, sessao)
    if lista_regras_validacao is not None:
        for regra in lista_regras_validacao:
            regra()            
    entidade_nova = criar_entidade_bd(entidade, schema, sessao)
    if lista_regras_pos is not None:
        for regra in lista_regras_pos:
            regra(entidade_nova, sessao)
    salvar_log_bd('criar', entidade.__tablename__, 'id', entidade_nova[nome_entidade]['id'], ator, sessao)
    return entidade_nova

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def visualizar_entidade(entidade, ator, sessao:Session, lista_campos: dict = None, lista_regras_validacao: list = None, lista_regras_pos:list=None):
    print('teste')
    verificar_permissao(ator, 'buscar', entidade, tipo=lista_campos['cargo'] if 'cargo' in lista_campos else None)
    if lista_regras_validacao is not None:
        for regra in lista_regras_validacao:
            regra()
    lista = exec_busca(entidade, lista_campos, sessao)
    if lista_regras_pos is not None:
        for regra in lista_regras_pos:
            regra(lista, sessao)
    return lista


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def editar_entidade(id, entidade, schema, ator, sessao: Session, lista_regras_validacao: list = None, lista_regras_pos:list=None):
    nome_entidade = entidade.__nome__
    verificar_permissao(ator, 'editar',nome_entidade, tipo='Não Classificado' if nome_entidade == 'Usuario' else None) #colocar validação para cargo internamente
    entidade_consultada = verificar_entidade_existe(id=id, sessao=sessao)
    campos = verificar_entidade_atualizacao(schema, entidade)
    if lista_regras_validacao is not None:
        for regra in lista_regras_validacao:
            regra()      
    edicao = editar_entidade_bd(schema=schema, entidade=entidade_consultada, campos=campos, sessao=sessao)
    if lista_regras_pos is not None:
        for regra in lista_regras_pos:
            regra(edicao, sessao)
    salvar_log_bd('editar', entidade.__tablename__, 'id', edicao[nome_entidade]['id'], ator, sessao)

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def ativar_entidade():
    pass

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def desativar_entidade():
    pass

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def autenticar_entidade():
    pass

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def atualizar_token():
    pass

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def solicitar_reset_senha():
    pass

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Inclui --> Fidelidade, Status
def atualizar_campo():
    pass