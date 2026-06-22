from Application.base import verificar_permissao, verificar_entidade_atualizacao

from Infrastructure.Repositories.base import ativar_entidade_bd, desativar_entidade_bd, editar_entidade_bd, verificar_entidade_criacao, criar_entidade_bd, Session, exec_busca, verificar_entidade_existe, verificar_subentidade_criacao
#Logs
from Infrastructure.Repositories.Registros.reLogs import salvar_log_bd

from Infrastructure.Models.Persona.mUsuario import Usuario
from Infrastructure.Models.base import TipoLogin

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Função de criar entidade (para quaisquer criações, exige permissão, a ser controlada pelo JSON)
def criar_entidade(entidade, schema, ator, sessao: Session, campo_verificacao: list=None, lista_regras_validacao: list = None, lista_regras_pos:list=None):
    nome_entidade = entidade.__name__
    verificar_permissao(ator, 'criar',nome_entidade, tipo='Não Classificado' if nome_entidade == 'Usuario' else None) #colocar validação para cargo internamente
    verificar_entidade_criacao(entidade, schema, nome_entidade, campo_verificacao, sessao)
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

def criar_subentidade(entidade, id_esq, id_dir, ator, sessao, campos_complementares=None, lista_regras_validacao: list=None, lista_regras_pos:list=None):
    nome_entidade = entidade.__name__
    if nome_entidade == 'UsuarioFilial':
        tipo = verificar_entidade_existe(Usuario, id_esq, sessao).cargo
    else:
        tipo=None
    verificar_permissao(ator, 'vincular', nome_entidade, tipo=tipo)
    verificar_subentidade_criacao()

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def visualizar_entidade(entidade, sessao:Session, ator:TipoLogin=None, lista_campos: dict = None, lista_regras_validacao: list = None, lista_regras_pos:list=None):
    verificar_permissao(ator, 'buscar', entidade.__name__, tipo=lista_campos['cargo'] if 'cargo' in lista_campos else None)
    if lista_regras_validacao is not None:
        for regra in lista_regras_validacao:
            regra(entidade, ator, lista_campos)
    lista = exec_busca(entidade, lista_campos, sessao)
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
    campos = verificar_entidade_atualizacao(schema, entidade_consultada)
    if lista_regras_validacao is not None:
        for regra in lista_regras_validacao:
            regra()      
    edicao = editar_entidade_bd(schema, nome_entidade, entidade_consultada, campos, sessao)
    if lista_regras_pos is not None:
        for regra in lista_regras_pos:
            regra(edicao, sessao)
    salvar_log_bd('editar', entidade.__tablename__, 'id', edicao[nome_entidade]['id'], ator, sessao)
    return edicao

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def ativar_entidade(entidade, ator, id: int, sessao: Session, lista_regras_validacao: list=None, lista_regras_pos: list=None):
    nome_entidade = entidade.__name__
    verificar_permissao(ator, 'ativar',nome_entidade, tipo='Não Classificado' if nome_entidade == 'Usuario' else None) #colocar validação para cargo internamente
    entidade_consultada = verificar_entidade_existe(entidade, id, sessao)
    if lista_regras_validacao is not None:
        for regra in lista_regras_validacao:
            regra()      
    ativo = ativar_entidade_bd(entidade_consultada,nome_entidade, sessao)
    if lista_regras_pos is not None:
        for regra in lista_regras_pos:
            regra(ativo, sessao)
    salvar_log_bd('ativar', entidade.__tablename__, 'id', ativo[nome_entidade]['id'], ator, sessao)
    return ativo

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def desativar_entidade(entidade, ator, id: int, sessao: Session, lista_regras_validacao: list=None, lista_regras_pos: list=None):
    nome_entidade = entidade.__name__
    verificar_permissao(ator, 'desativar',nome_entidade, tipo='Não Classificado' if nome_entidade == 'Usuario' else None) #colocar validação para cargo internamente
    entidade_consultada = verificar_entidade_existe(entidade, id, sessao)
    if lista_regras_validacao is not None:
        for regra in lista_regras_validacao:
            regra()      
    desativo = desativar_entidade_bd(entidade_consultada,nome_entidade, sessao)
    if lista_regras_pos is not None:
        for regra in lista_regras_pos:
            regra(desativo, sessao)
    salvar_log_bd('desativar', entidade.__tablename__, 'id', desativo[nome_entidade]['id'], ator, sessao)
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