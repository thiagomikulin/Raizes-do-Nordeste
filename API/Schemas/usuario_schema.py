from pydantic import BaseModel

class LoginSchema(BaseModel):
    nome:str
    email:str
    senha:str
    ativo:bool
    cargo:str

    class Config:
        from_attributes=True