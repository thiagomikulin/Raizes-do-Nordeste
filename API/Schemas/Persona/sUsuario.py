from API.Schemas.base import *
from Infrastructure.Models.Persona.mUsuario import Cargo

class LoginSchema(BaseModel):
    email:str = Field(min_length=10)
    senha:str = Field(min_length=3)

    class Config:
        from_attributes=True

class CriacaoSchema(BaseModel):
    nome: str = Field( min_length=10)
    email: str = Field(min_length=10)
    senha: str = Field(min_length=3)

    class Config:
        from_attributes = True

class EdicaoSchema(BaseModel):
    nome: str = Field(min_length=10)
    email: str = Field(min_length=14)
    cargo: Cargo