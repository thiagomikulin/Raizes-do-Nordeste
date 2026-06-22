from fastapi import Request
from fastapi.responses import JSONResponse
import MySQLdb

from datetime import datetime
from typing import Optional

from Infrastructure.Models.Persona.mUsuario import Usuario

from main import app

# https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers


class ExceptionHTTP(Exception):
    def __init__(self, code, error:str, message:str, detail: list):
        self.code = code
        self.error = error
        self.message = message
        self.detail = detail

@app.exception_handler(ExceptionHTTP)
async def handler_de_excecao(request: Request, exc: ExceptionHTTP):
    return JSONResponse(
        status_code=exc.code,
        content={
            "error":exc.error,
            "message":exc.message,
            "details":exc.detail,
            "timestamp":datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            "path":request.url.path
        }
    )

#Opcional, já retorna no ExceptionGenerica
# @app.exception_handler(MySQLdb.IntegrityError)
# async def handler_excecao_db(request: Request, exc: MySQLdb.Error):
#     return JSONResponse(
#         status_code=exc.code,
#         content={
#             "error":exc.error,
#             "message":exc.message,
#             "details":exc.detail,
#             "timestamp":datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
#             "path":request.url.path
#         }
#     )

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Exceptions

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
    def __init__(self, entidade):
        super().__init__(
            code=400,
            error=f"NÃO ALTERADO",
            message=f"O {type(entidade).__name__} enviado é idêntico ao salvo, portanto a requisição não será realizada!",
            detail=[
                {"field":f"{entidade.id}","issue":"identical value"}
            ],
        )

# 401
class NaoAutenticado(ExceptionHTTP):
    def __init__(self):
        super().__init__(
            code = 401,
            error="NÃO AUTENTICADO",
            message=f"É necessário estar autenticado para realizar esta ação!",
            detail=[
                {"field":"token","issue":"invalid token"}
            ],
        )


class AcessoInvalido(ExceptionHTTP):
    def __init__(self):
        super().__init__(
            code=401,
            error='ACESSO INVÁLIDO',
            message='Senha Incorreta! Tente novamente ou reinicie a senha!',
            detail=[
                {"field":"password", "issue":"incorrect"}
            ],
        )
    
#-----------------------------------------------------------------------------------------

#404

class Desativado(ExceptionHTTP):
    def __init__(self):
        super().__init__(
            code=404,
            error='ACESSO INATIVO',
            message='Parece que seu acesso foi desativado! Entre em contato com a equipe técnica!',
            detail=[
                {"field":"ativo", "issue":"deactivated"}
            ],
        )

class AcessoNaoEncontrado(ExceptionHTTP):
    def __init__(self):
        super().__init__(
            code=404,
            error='ACESSO NÃO ENCONTRADO',
            message='Seu acesso não foi localizado em nosso sistema! Entre em contato com a equipe técnica!',
            detail=[
                {"field":"email", "issue":"not found"}
            ],
        )

class NaoEncontrado(ExceptionHTTP):
    def __init__(self, campos:dict):
        super().__init__(
            code=404,
            error='NÃO ENCONTRADO',
            message=f'A busca realizada não foi localizada em nosso sistema! Entre em contato com a equipe técnica!',
            detail=campos,
        )

#detail=[{"field":chave, "issue":f" '{campos[chave]}' not found" for chave, valor in campos} ],

class SchemaInvalido(ExceptionHTTP):
    def __init__(self, schema):
        super().__init__(
            code = 400,
            error='CAMPOS PREENCHIDOS INCORRETAMENTE',
            message="Os campos não foram preenchidos corretamente! Verifique e tente novamente",
            detail=[{"field":attr, "issue":"required"} for attr, val in schema.__dict__.items() if not val and schema.model_fields[attr].is_required()], #Retorna o atributo na lista de atributos e valores se o valor não existir
        )

class CamposObrigatorios(ExceptionHTTP):
    def __init__(self, campos):
        super().__init__(
            code = 400,
            error='CAMPOS PREENCHIDOS INCORRETAMENTE',
            message="Alguns campos obrigatórios requisitados não foram preenchidos! Tente novamente",
            detail=[{"field":attr, "issue":f"{val} required"} for attr, val in campos.items()],
        )

class SemPermissao(ExceptionHTTP):
    def __init__(self, ator, permissao:str):
        super().__init__(
            code=403,
            error='NÃO AUTORIZADO',
            message=f'Seu acesso não tem permissão para {permissao} este conteúdo! Entre em contato com a equipe técnica!',
            detail=[
                {'field':'cargo' if type(ator)==Usuario else 'cliente', 'issue': 'not authorized'}
            ],
        )

class Conflito(ExceptionHTTP):
    def __init__(self, entidade, encontrados: dict):
        lista = [f'{chave} = {valor}' for chave, valor in encontrados.items()]
        if len(lista) > 1:
            descricao = " e ".join(lista)
        else:
            descricao = lista[0]
        print('teste')
        mensagem = f'Já existe um {entidade} com {descricao} cadastrado no sistema'
        super().__init__(
            code=409,
            error=f"CONFLITO DE CRIAÇÃO DE {entidade.upper()}",
            message=mensagem,
            detail=[
                {"field":campo,"issue":"duplicated value"} for campo, valor in encontrados.items()
            ],
        )

class NaoAtivo(ExceptionHTTP):
    def __init__(self, ator):
        super().__init__(
            code=500,
            error="ACESSO DESATIVADO",
            message="Parece que este acesso foi desativado! Entre em contato com o suporte!",
            detail=[
                {"field":f"{type(ator).__name__}","issue":"deactivated"}
            ],
        )

class ExceptionGenerica(ExceptionHTTP):
    def __init__(self, exception: Exception):
        super().__init__(
            code=500,
            error="ERRO INTERNO",
            message="Ops! Parece que algo deu errado",
            detail=[
                {"field":"exception","issue":str(exception)}
            ],
        )

class ExceptionRequest(ExceptionHTTP):
    def __init__(self, retorno):
        super().__init__(
            code=retorno.status,
            error=retorno.error,
            message="Ops! Parece que algo deu errado",
            detail=[
                {"field":"exception","issue":str(exception)}
            ],
        )


class SenhaCurta(ExceptionHTTP):
    def __init__(self):
        super().__init__(
            code=404,
            error='SENHA DESPADRONIZADA',
            message='A senha precisa ter pelo menos 8 caracteres',
            detail=[
                {"field":"senha", "issue":"invalid format"}
            ],
        )

class FormatoInvalido(ExceptionHTTP):
    def __init__(self, campo):
        super().__init__(
            code=404,
            error=f'{campo} Inválido',
            message=f'Este {campo} não usa o formato padrão! Tente novamente!',
            detail=[
                {"field":campo.lower(), "issue":"invalid format"}
            ],
        )