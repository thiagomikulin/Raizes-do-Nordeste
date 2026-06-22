from pydantic import BaseModel, validator, model_validator, Field, field_validator
from typing import Optional
from datetime import date
from enum import Enum
import re

def validar_cpf(cpf):
    padrao = r'^\d{3}\.\d{3}\.\d{3}\-\d{2}$'
    if not re.match(padrao, cpf):
        return False
    else:
        return True
    
def validar_email(email):
    padrao = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+|.[A-Za-z]{2,7}'
    if not re.fullmatch(padrao, email):
        return False
    else:
        return True