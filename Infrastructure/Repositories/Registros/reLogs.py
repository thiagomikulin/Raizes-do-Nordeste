from Infrastructure.Repositories.base import Session

from Infrastructure.Models.Registros.mLogs import Log

def salvar_log_bd(acao, tabela, campo, valor_novo, ator, sessao: Session, valor_ant=''):
    novo_log = Log(acao, tabela, campo, valor_ant, valor_novo, type(ator).__name__, ator.id)
    sessao.add(novo_log)
    sessao.commit()
    return True