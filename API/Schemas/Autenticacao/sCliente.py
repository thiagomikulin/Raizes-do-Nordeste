from API.Schemas.base import *


class CriacaoSchema(BaseModel):
    nome: str
    email: str
    cpf: str
    scanFace:str
    senha:str
    endereco:str
    fidelidade:str
    # data_nasc:
    ativo: bool

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    cpf: Optional[str]
    email: Optional[str]
    scanFace: Optional[str]
    senha: str

    class Config:
        from_attributes = True