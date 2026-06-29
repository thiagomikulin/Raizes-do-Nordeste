from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Enum as AlEnum, Date, LargeBinary, and_
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.inspection import inspect
from enum import Enum as EnumPy
import datetime



# BD de teste (para desenvolvimento apenas)
# db = create_engine('mysql://root:root@localhost:3306/raizes_do_nordeste')

#Base do banco
Base = declarative_base()

class TipoLogin(str, EnumPy):
    USUARIO = "Usuario"
    CLIENTE = "Cliente"

