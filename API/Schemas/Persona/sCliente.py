from API.Schemas.base import *
from Domain.__exceptions__ import FormatoInvalido


class CriacaoSchema(BaseModel):
    nome: str = Field(min_length=10)
    email: str 
    cpf: str = Field()
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
    nome: str = Field(min_length=10)
    email: str = Field(min_length=10)
    endereco:str
    data_nasc:date
    

    