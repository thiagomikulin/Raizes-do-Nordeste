from Models.base import Base, Column, ForeignKey

class UsuarioFilial(Base):
    usuario = Column('IdUsuario', ForeignKey('usuarios.id'))
    filial = Column('IdFilial'), ForeignKey('filiais.id')

    def __init__(self, usuario_id, filial_id):
        self.usuario = usuario_id
        self.filial = filial_id