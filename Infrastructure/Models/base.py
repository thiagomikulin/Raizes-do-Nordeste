from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType 
#Tentar ver forma de fazer ChoiceType funcionar

#Criação do BD
db = create_engine('mysql:///Database/database.db')

#Base do banco
Base = declarative_base()