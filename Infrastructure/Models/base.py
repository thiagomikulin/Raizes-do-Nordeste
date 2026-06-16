from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Enum as AlEnum, Date
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum as EnumPy
import datetime


#Criação do BD
db = create_engine('mysql://root:root@localhost:3306/raizes_do_nordeste')

#Base do banco
Base = declarative_base()

Base.metadata.create_all(db)

class TipoLogin(str, EnumPy):
    USUARIO = "Usuario"
    CLIENTE = "Cliente"

