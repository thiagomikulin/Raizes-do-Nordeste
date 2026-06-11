from pydantic import BaseModel

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