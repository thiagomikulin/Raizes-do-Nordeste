from fastapi import Request
from fastapi.responses import JSONResponse

from datetime import datetime
from typing import Optional

from Infrastructure.Models.Persona.mUsuario import Usuario

from main import app

# https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers


class ExceptionHTTP(Exception):
    def __init__(self, code, error:str, message:str, detail: list, path):
        self.code = code
        self.error = error
        self.message = message
        self.detail = detail
        self.path = path

@app.exception_handler(ExceptionHTTP)
async def handler_de_excecao(request: Request, exc: ExceptionHTTP):
    return JSONResponse(
        status_code=exc.code,
        content={
            "error":exc.error,
            "message":exc.message,
            "details":exc.detail,
            "timestamp":datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            "path":exc.path
        }
    )

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Exceptions

class SchemaExcept(Exception):
    pass

class PermissionExcept(Exception):
    pass

class ConflictExcept(Exception):
    pass

class NotFoundExcept(Exception):
    def __init__(self, **kwargs):
        self.campos = kwargs

class IncorrectPWExcept(Exception):
    pass

class UnalteredExcept(Exception):
    pass

class MandatoryForFillingExcept(Exception):
    def __init__(self, campos):
        self.campos = campos

#==============================================================================================

#Exceções HTTP

class NaoAlterado(ExceptionHTTP):
    def __init__(self, entidade, path):
        super().__init__(
            code=400,
            error=f"NÃO ALTERADO",
            message=f"O {entidade} enviado é idêntico ao salvo, portanto a requisição não será realizada!",
            detail=[
                {"field":f"{entidade}","issue":"identical value"}
            ],
            path=path
        )

# 401
class NaoAutenticado(ExceptionHTTP):
    def __init__(self, path):
        super().__init__(
            code = 401,
            error="NÃO AUTENTICADO",
            message=f"É necessário estar autenticado para realizar esta ação!",
            detail=[
                {"field":"token","issue":"invalid token"}
            ],
            path=path
        )


class AcessoInvalido(ExceptionHTTP):
    def __init__(self, path):
        super().__init__(
            code=401,
            error='ACESSO INVÁLIDO',
            message='Senha Incorreta! Tente novamente ou reinicie a senha!',
            detail=[
                {"field":"password", "issue":"incorrect"}
            ],
            path=path
        )
    
#-----------------------------------------------------------------------------------------

#404

class Desativado(ExceptionHTTP):
    def __init__(self, path):
        super().__init__(
            code=404,
            error='ACESSO INATIVO',
            message='Parece que seu acesso foi desativado! Entre em contato com a equipe técnica!',
            detail=[
                {"field":"ativo", "issue":"deactivated"}
            ],
            path=path
        )

class AcessoNaoEncontrado(ExceptionHTTP):
    def __init__(self, path):
        super().__init__(
            code=404,
            error='ACESSO NÃO ENCONTRADO',
            message='Seu acesso não foi localizado em nosso sistema! Entre em contato com a equipe técnica!',
            detail=[
                {"field":"email", "issue":"not found"}
            ],
            path=path
        )

class NaoEncontrado(ExceptionHTTP):
    def __init__(self, path, campos):
        chave= list(campos.keys())[0]
        super().__init__(
            code=404,
            error='NÃO ENCONTRADO',
            message=f'O {path[1:-2]} com este filtro não foi localizado em nosso sistema! Entre em contato com a equipe técnica!',
            detail=[{"field":chave, "issue":f" '{campos[chave]}' not found"}],
            path=path
        )



class SchemaInvalido(ExceptionHTTP):
    def __init__(self, schema, path):
        super().__init__(
            code = 400,
            error='CAMPOS PREENCHIDOS INCORRETAMENTE',
            message="Os campos não foram preenchidos corretamente! Verifique e tente novamente",
            detail=[{"field":attr, "issue":"required"} for attr, val in schema.__dict__.items() if not val and schema.model_fields[attr].is_required()], #Retorna o atributo na lista de atributos e valores se o valor não existir
            path=path
        )

class CamposObrigatorios(ExceptionHTTP):
    def __init__(self, campos, path):
        super().__init__(
            code = 400,
            error='CAMPOS PREENCHIDOS INCORRETAMENTE',
            message="Alguns campos obrigatórios requisitados não foram preenchidos! Tente novamente",
            detail=[{"field":attr, "issue":f"{val} required"} for attr, val in campos.items()],
            path=path
        )

class SemPermissao(ExceptionHTTP):
    def __init__(self, path, ator):
        super().__init__(
            code=403,
            error='NÃO AUTORIZADO',
            message=f'Seu acesso não tem permissão para {'gerar' if 'criar' in path else 'verificar'} este conteúdo! Entre em contato com a equipe técnica!',
            detail=[
                {'field':'cargo' if type(ator)==Usuario else 'cliente', 'issue': 'not authorized'}
            ],
            path=path
        )

class Conflito(ExceptionHTTP):
    def __init__(self, entidade, campo, valor_campo, path):
        super().__init__(
            code=409,
            error=f"CONFLITO DE CRIAÇÃO DE {entidade.upper()}",
            message=f"Já existe um {entidade} com {campo} {valor_campo} cadastrado no sistema",
            detail=[
                {"field":"email","issue":"duplicated value"}
            ],
            path=path
        )

class ExceptionGenerica(ExceptionHTTP):
    def __init__(self, exception: Exception, path):
        super().__init__(
            code=500,
            error="ERRO INTERNO",
            message="Ops! Parece que algo deu errado",
            detail=[
                {"field":"exception","issue":str(exception)}
            ],
            path=path
        )