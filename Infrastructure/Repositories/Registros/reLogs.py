from Infrastructure.Repositories.base import Session

from Infrastructure.Models.Registros.mLogs import Log

def salvar_log_bd(acao, tabela, valor_novo, ator, sessao: Session,campos:list=None, valor_ant=None, campo_id='id'):
    print(f'''
    acao: {acao},
    tabela: {tabela},
    valor_novo: {valor_novo},
    ator: {ator},
    sessao: {sessao}, 
    campos: {campos},
    valor_ant: {valor_ant}
    ''')
    campo_salvo = ', '.join(campos)
    for item in range(0, len(campos)):
        print(campos[item])
        #Identificação dos novos itens
        lista_novos = [valor_novo[campo] for campo in campos]
        print(lista_novos)

        #Identificação de valores antigos (se houver)
        if valor_ant is not None:
            lista_antigos = [valor_ant[campo] for campo in campos]
        else:
            lista_antigos = ''

        print(lista_novos)
        print('aqui')
        lista_novos = [str(item) for item in lista_novos]
        print(lista_novos)
        if len(lista_novos) > 1:
            novos = ' , '.join(lista_novos)
            if valor_ant is not None:
                lista_antigos = [str(item) for item in lista_antigos]
                antigos = ' , '.join(lista_antigos)
            else:
                antigos = ''
        else:
            novos = lista_novos[item]
            if valor_ant is not None:
                antigos = lista_antigos[item]
            else:
                antigos = ''

        novo_log = Log(
            acao, 
            tabela, 
            valor_novo[campo_id],
            f'{campo_salvo}',
            f'{antigos}', 
            f'{novos}', 
            type(ator).__name__, 
            str(ator.id))
        print('aqui')
        sessao.add(novo_log)
    sessao.commit()
    return True