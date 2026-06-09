from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.orm import declarative_base


#Criação do BD
db = create_engine('mysql://root:root@localhost:3306/raizes_do_nordeste')

#Base do banco
Base = declarative_base()

Base.metadata.create_all(db)


        