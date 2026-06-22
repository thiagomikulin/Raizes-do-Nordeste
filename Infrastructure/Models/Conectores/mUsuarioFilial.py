from Infrastructure.Models.base import Base, Column, ForeignKey

class UsuarioFilial(Base):
    __tablename__ = 'usuariosFiliais'

    usuario = Column('IdUsuario', ForeignKey('usuarios.ID'), primary_key=True)
    filial = Column('IdFilial', ForeignKey('filiais.ID'), primary_key=True)

    def __init__(self, usuario, filial):
        self.usuario = usuario #id
        self.filial = filial #id