from Infrastructure.Repositories.base import Session

from Infrastructure.Models.Registros.mLogs import Logs

def salvar_log_bd(sessao: Session):
    novo_log = Log()
    sessao.add(novo_log)
    sessao.commit()
    return True