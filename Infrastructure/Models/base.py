from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, Float, ForeignKey, Enum as AlEnum
from sqlalchemy.orm import declarative_base
from enum import Enum as EnumPy


#Criação do BD
db = create_engine('mysql://root:root@localhost:3306/raizes_do_nordeste')

#Base do banco
Base = declarative_base()

Base.metadata.create_all(db)


        