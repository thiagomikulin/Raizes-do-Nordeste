from API.Schemas.base import *

class LoginSchema(BaseModel):
    email:str
    senha:str

    class Config:
        from_attributes=True

class CriacaoSchema(BaseModel):
    nome: str
    email: str
    senha: str

    class Config:
        from_attributes = True

class EdicaoSchema(BaseModel):
    nome: str
    email: str
    cargo: str