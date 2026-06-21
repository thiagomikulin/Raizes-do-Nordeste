from API.Schemas.base import *
from Domain.__exceptions__ import SenhaCurta, FormatoInvalido


class CriacaoSchema(BaseModel):
    nome: str = Field(default='Seu Nome', min_length=15)
    email: str = Field(default='seuemail@dominio.com', min_length=15)
    cpf: str = Field(default='999.999.999-99')
    scanFace:Optional[str]
    senha:str
    endereco:Optional[str]
    data_nasc:Optional[date]

    class Config:
        from_attributes = True

    @validator('cpf')
    def verificar_formato_cpf(cls, cpf):
        if not validar_cpf(cpf):
            raise FormatoInvalido('CPF')
        
    @validator('email')
    def verificar_formato_email(cls, email):
        if not validar_email(email):
            raise FormatoInvalido('Email')


class LoginSchema(BaseModel):
    cpf: Optional[str]
    email: Optional[str]
    scanFace: Optional[str]
    senha: str

    class Config:
        from_attributes = True

    @model_validator(mode='after')
    def verificar_campos_login(self):
        cpf = self.cpf
        email = self.email
