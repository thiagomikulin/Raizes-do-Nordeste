from enum import Enum

from Application.base import verificar_permissao, verificar_entidade_atualizacao

from Infrastructure.Repositories.base import ativar_entidade_bd, desativar_entidade_bd, editar_entidade_bd, excluir_entidade_bd, verificar_entidade, criar_entidade_bd, Session, exec_busca, verificar_entidade_existe
#Logs
from Infrastructure.Repositories.Registros.reLogs import salvar_log_bd

from Infrastructure.Models.Persona.mUsuario import Usuario
from Infrastructure.Models.base import TipoLogin

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Função de criar entidade (para quaisquer criações, exige permissão, a ser controlada pelo JSON)
def criar_entidade(entidade, schema, ator, sessao: Session, campo_verificacao: list=None, lista_regras_validacao: list = None, lista_regras_pos:list=None):
    nome_entidade = entidade.__name__
    verificar_permissao(ator, 'criar',nome_entidade, tipo='Não Classificado' if nome_entidade in ['Usuario', 'UsuarioFilial'] else None) #colocar validação para cargo internamente
    verificar_entidade(entidade, schema, nome_entidade, campo_verificacao, sessao, 'criar')
    if lista_regras_validacao is not None:
        for regra in lista_regras_validacao:
            regra()            
    entidade_nova = criar_entidade_bd(entidade, schema, sessao, ator)
    if lista_regras_pos is not None:
        for regra in lista_regras_pos:
            regra(entidade_nova, sessao)
    if nome_entidade in ['UsuarioFilial', 'PromoFilial', 'ItemReceita', 'VariacaoFilial']:
        id = campo_verificacao
        campo_id = campo_verificacao[0]
        print(campo_id)
    else:
        id = ['id']
        campo_id = 'id'
    salvar_log_bd('criar', entidade.__tablename__, entidade_nova[nome_entidade], ator, sessao, id, campo_id=campo_id)
    return entidade_nova

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#OBS: ESTA FUNÇÃO SERÁ USADA APENAS PARA APAGAR RELAÇÕES A PRINCÍPIO (EX: UsuarioFilial, ItemReceita, etc)
def excluir_entidade(entidade, schema, ator, sessao: Session, campo_verificacao: list=None, lista_regras_validacao: list = None, lista_regras_pos:list=None):
    nome_entidade = entidade.__name__
    verificar_permissao(ator, 'excluir',nome_entidade, tipo='Não Classificado' if nome_entidade in ['Usuario', 'UsuarioFilial'] else None) #colocar validação para cargo internamente
    verificar_entidade(entidade, schema, nome_entidade, campo_verificacao, sessao, 'excluir')
    if lista_regras_validacao is not None:
        for regra in lista_regras_validacao:
            regra()            
    entidade_excluida = excluir_entidade_bd(entidade, schema, sessao)
    if lista_regras_pos is not None:
        for regra in lista_regras_pos:
            regra(entidade_excluida, sessao)
    # if nome_entidade in ['UsuarioFilial']:
    #     id = campo_verificacao
    # else:
    #     id = ['id']
    # salvar_log_bd('criar', entidade.__tablename__, entidade_excluida[nome_entidade], ator, sessao, id)
    return entidade_excluida

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def visualizar_entidade(entidade, sessao:Session, ator:TipoLogin=None, lista_campos: dict = None, lista_regras_validacao: list = None, lista_regras_pos:list=None):
    permissoes = verificar_permissao(ator, 'buscar', entidade.__name__, tipo=lista_campos['cargo'] if 'cargo' in lista_campos else None)
    if lista_regras_validacao is not None:
        for regra in lista_regras_validacao:
            regra(entidade, ator, lista_campos)
    lista = exec_busca(entidade, lista_campos, sessao, permissoes)
    #Ordenação do retorno
    if lista_regras_pos is not None:
        for regra in lista_regras_pos:
            regra(lista, sessao)
    return lista


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def editar_entidade(id, entidade, schema, ator, sessao: Session, lista_regras_validacao: list = None, lista_regras_pos:list=None):
    nome_entidade = entidade.__name__
    verificar_permissao(ator, 'editar',nome_entidade, tipo='Não Classificado' if nome_entidade == 'Usuario' else None) #colocar validação para cargo internamente
    entidade_consultada = verificar_entidade_existe(entidade, id=id, sessao=sessao)
    campos_antigos = {chave:valor.value if isinstance(valor, Enum) else valor
                        for chave, valor in entidade_consultada.__dict__.items() 
                        if chave not in ['senha', 'cpf', 'conta_banc']}
    campos = verificar_entidade_atualizacao(schema, entidade_consultada)
    if lista_regras_validacao is not None:
        for regra in lista_regras_validacao:
            regra()      
    
    edicao = editar_entidade_bd(schema, nome_entidade, entidade_consultada, campos, sessao, ator)
    if lista_regras_pos is not None:
        for regra in lista_regras_pos:
            regra(edicao, sessao)
    print('teste2323232')
    salvar_log_bd('editar', entidade.__tablename__, edicao[nome_entidade], ator, sessao, campos, campos_antigos, id)
    return edicao

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def ativar_entidade(entidade, ator, id: int, sessao: Session, lista_regras_validacao: list=None, lista_regras_pos: list=None):
    nome_entidade = entidade.__name__
    verificar_permissao(ator, 'ativar',nome_entidade, tipo='Não Classificado' if nome_entidade == 'Usuario' else None) #colocar validação para cargo internamente
    entidade_consultada = verificar_entidade_existe(entidade, id, sessao)
    campos_antigos = {chave:valor for chave, valor in entidade_consultada.__dict__.items()}
    if lista_regras_validacao is not None:
        for regra in lista_regras_validacao:
            regra()      
    ativo = ativar_entidade_bd(entidade_consultada,nome_entidade, sessao)
    if lista_regras_pos is not None:
        for regra in lista_regras_pos:
            regra(ativo, sessao)
    salvar_log_bd('ativar', entidade.__tablename__, ativo[nome_entidade], ator, sessao, ['ativo'], campos_antigos)
    return ativo

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def desativar_entidade(entidade, ator, id: int, sessao: Session, lista_regras_validacao: list=None, lista_regras_pos: list=None):
    nome_entidade = entidade.__name__
    verificar_permissao(ator, 'desativar',nome_entidade, tipo='Não Classificado' if nome_entidade == 'Usuario' else None) #colocar validação para cargo internamente
    entidade_consultada = verificar_entidade_existe(entidade, id, sessao)
    campos_antigos = {chave:valor for chave, valor in entidade_consultada.__dict__.items()}
    if lista_regras_validacao is not None:
        for regra in lista_regras_validacao:
            regra()      
    desativo = desativar_entidade_bd(entidade_consultada,nome_entidade, sessao)
    if lista_regras_pos is not None:
        for regra in lista_regras_pos:
            regra(desativo, sessao)
    salvar_log_bd('desativar', entidade.__tablename__, desativo[nome_entidade], ator, sessao, ['ativo'], campos_antigos)
    return desativo

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