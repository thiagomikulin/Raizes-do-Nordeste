from API.Schemas.base import *


class CriacaoSchema(BaseModel):
    nome: str
    email: str
    cpf: str
    scanFace:Optional[str]
    senha:str
    endereco:Optional[str]
    data_nasc:Optional[date]

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    cpf: Optional[str]
    email: Optional[str]
    scanFace: Optional[str]
    senha: str

    class Config:
        from_attributes = True