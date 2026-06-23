from Infrastructure.Models.base import Base, Column, Integer, String, AlEnum, EnumPy, Boolean

class PeriodoAno(str, EnumPy):
    VERAO = 'Verão'
    OUTONO = 'Outono'
    INVERNO = 'Inverno'
    PRIMAVERA = 'Primavera'

class Ingrediente(Base):
    __tablename__ = 'ingredientes'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    nome = Column('Nome', String(80), nullable=False)
    periodo = Column('Periodo', AlEnum(PeriodoAno, values_callable=lambda enum: [e.value for e in enum]), nullable=False)
    ativo = Column('Ativo', Boolean, default=True)

    def __init__(self, nome, periodo):
        self.nome = nome
        self.periodo = periodo