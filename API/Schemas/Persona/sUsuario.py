from API.Schemas.base import *
from Infrastructure.Models.Persona.mUsuario import Cargo
from Domain.__exceptions__ import SenhaCurta

class LoginSchema(BaseModel):
    email:str = Field(default='seuemail@dominio.com', min_length=15)
    senha:str = Field(default='senhade8caracteres', min_length=8)

    class Config:
        from_attributes=True

class CriacaoSchema(BaseModel):
    nome: str = Field(default='Seu Nome', min_length=15)
    email: str = Field(default='seuemail@dominio.com', min_length=15)
    senha: str = Field(default='senhade8caracteres', min_length=8)

    class Config:
        from_attributes = True

class EdicaoSchema(BaseModel):
    nome: str = Field(default='Nome a alterar', min_length=15)
    email: str = Field(default='seuemail@dominio.com', min_length=15)
    cargo: Cargo