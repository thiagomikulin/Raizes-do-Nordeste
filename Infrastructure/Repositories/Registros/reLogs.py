from Infrastructure.Repositories.base import Session

from Infrastructure.Models.Registros.mLogs import Log

def salvar_log_bd(acao, tabela, valor_novo, ator, sessao: Session,campos:list=None, valor_ant=''):
    campo_salvo = ', '.join(campos)
    for item in range(0, len(campos)):
        lista_novos = [f'{valor_novo[campo]}' for campo in campos]
        print(lista_novos)
        if len(lista_novos) > 1:
            novos = ' , '.join(lista_novos)
            print(novos)
        else:
            novos = lista_novos[item]
        novo_log = Log(
            acao, 
            tabela, 
            f'{campo_salvo}',
            f'{valor_ant}', 
            f'{novos}', 
            type(ator).__name__, 
            str(ator.id))
        sessao.add(novo_log)
    sessao.commit()
    return True