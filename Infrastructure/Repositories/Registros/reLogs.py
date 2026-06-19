from Infrastructure.Repositories.base import Session

from Infrastructure.Models.Registros.mLogs import Log

def salvar_log_bd(acao, tabela, campo, valor_novo, ator, sessao: Session, valor_ant=''):
    if type(campo) == list:
        for item in range(0, len(campo)+1):
            novo_log = Log(acao, tabela, campo, str(campo[item]), str(valor_novo[campo[item]]), type(ator).__name__, str(ator.id))
            sessao.add(novo_log)
        sessao.commit()
    else:
        novo_log = Log(acao, tabela, campo, str(valor_ant), str(valor_novo), type(ator).__name__, str(ator.id))
        sessao.add(novo_log)
        sessao.commit()
    return True