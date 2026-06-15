from Models.base import Base, Column, ForeignKey

class UsuarioFilial(Base):
    __tablename__ = 'usuariosFiliais'

    usuario = Column('IdUsuario', ForeignKey('usuarios.id'), primary_key=True)
    filial = Column('IdFilial', ForeignKey('filiais.id'), primary_key=True)

    def __init__(self, usuario_id, filial_id):
        self.usuario = usuario_id
        self.filial = filial_id