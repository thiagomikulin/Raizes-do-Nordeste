from API.Schemas.base import *
from Domain.__exceptions__ import SenhaCurta, FormatoInvalido


class CriacaoSchema(BaseModel):
    nome: str = Field(default='Seu Nome', min_length=15)
    email: str = Field(default='seuemail@dominio.com', min_length=15)
    cpf: str = Field(default='999.999.999-99')
    scanFace:Optional[str]
    senha:str
    endereco:Optional[str]
    data_nasc:Optional[date] = None

    class Config:
        from_attributes = True

    @field_validator("data_nasc", mode="before")
    def converter_vazio_para_none(cls, v):
        if v == "":
            return None
        return v

    @validator('cpf')
    def verificar_formato_cpf(cls, cpf):
        if not validar_cpf(cpf):
            raise FormatoInvalido('CPF')
        return cpf
        
    @validator('email')
    def verificar_formato_email(cls, email):
        if not validar_email(email):
            raise FormatoInvalido('Email')
        return email


class LoginSchema(BaseModel):
    cpf: Optional[str]
    email: Optional[str]
    scanFace: Optional[str]
    senha: str

    class Config:
        from_attributes = True

    # @model_validator(mode='after')
    # def verificar_campos_login(self):
    #     cpf = self.cpf
    #     email = self.email


class EdicaoSchema(BaseModel):
    nome: str = Field(default='Nome a alterar', min_length=15)
    email: str = Field(default='seuemail@dominio.com', min_length=15)
    cpf: str = Field(default='999.999.999-99', min_length=14)
    endereco:str = Field(default='Rua ______, Nº __, Complemento ___')
    fidelidade: int = Field(default=0)
    data_nasc:date = Field(default='1900-01-01')
    

    