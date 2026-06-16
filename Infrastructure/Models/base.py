from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Enum as AlEnum, Date
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum as EnumPy
import datetime


#Criação do BD
db = create_engine('mysql+mysqldb://user:password@mysql:3306/mydb')

#Base do banco
Base = declarative_base()

class TipoLogin(str, EnumPy):
    USUARIO = "Usuario"
    CLIENTE = "Cliente"

