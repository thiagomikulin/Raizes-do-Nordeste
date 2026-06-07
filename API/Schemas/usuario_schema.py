from pydantic import BaseModel

class LoginSchema(BaseModel):
    nome:str
    email:str
    senha:str
    ativo:bool
    cargo:str

    class Config:
        from_attributes=True

class CriacaoSchema(BaseModel):
    Nome: str
    Email: str
    Senha: str

    class Config:
        from_attributes = True

# {
#     "Nome":"nome_do_usuario",
#     "email":"email_do_usuario@dominio.com",
#     "senha":"senha_do_usuario",
# }