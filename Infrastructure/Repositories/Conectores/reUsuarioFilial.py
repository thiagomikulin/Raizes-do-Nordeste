from Infrastructure.Repositories.base import Session

from Infrastructure.Models.Conectores.mUsuarioFilial import *

from Domain.exceptions import ConflictExcept

def verificar_vinculo_filial(id_usuario, id_filial, sessao: Session):
    vinculo = sessao.query(UsuarioFilial).filter(UsuarioFilial.usuario == id_usuario and UsuarioFilial.filial == id_filial).first()
    if vinculo:
        raise ConflictExcept