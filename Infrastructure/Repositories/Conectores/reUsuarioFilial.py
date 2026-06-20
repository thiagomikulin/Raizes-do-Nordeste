from Infrastructure.Repositories.base import Session

from Infrastructure.Models.Conectores.mUsuarioFilial import UsuarioFilial

from Domain.exceptions import Conflito

def vincular_filial_bd(id_usuario, id_filial, sessao: Session):
    print('teste')
    usu_fil = UsuarioFilial(id_usuario, id_filial)
    sessao.add(usu_fil)
    sessao.commit()
    return {
        "message": "Vínculo criado com sucesso!",
        "vínculo":{
            "id_usuario":usu_fil.usuario,
            "id_filial":usu_fil.filial
        }
    }
    
    
def desvincular_filial_bd(usufil: UsuarioFilial, sessao: Session):
    sessao.delete(usufil)
    sessao.commit()
    return {
        "message": "Vínculo excluido com sucesso!",
        "vínculo":{
            "id_usuario":usufil.usuario,
            "id_filial":usufil.filial
        }
    }


def verificar_vinculo_filial(id_usuario, id_filial, sessao: Session):
    vinculo = sessao.query(UsuarioFilial).filter(UsuarioFilial.usuario == id_usuario and UsuarioFilial.filial == id_filial).first()
    if vinculo:
        raise Conflito('Vínculo Usuário/Filial', 'vínculo de usuário - filial', f'{id_usuario}/{id_filial}')
    return vinculo
    

def verificar_vinculo_filial_desv(id_usuario, id_filial, sessao: Session):
    vinculo = sessao.query(UsuarioFilial).filter(UsuarioFilial.usuario == id_usuario and UsuarioFilial.filial == id_filial).first()
    return vinculo