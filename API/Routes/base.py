from fastapi import HTTPException, APIRouter, Request
from fastapi.responses import JSONResponse

from datetime import datetime

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

#Padrões de erro geral

class SchemaInvalido(ExceptionHTTP):
    def __init__(self, schema, path):
        super().__init__(
            code = 400,
            error='CAMPOS PREENCHIDOS INCORRETAMENTE',
            message="Os campos não foram preenchidos corretamente! Verifique e tente novamente",
            detail=[{"field":attr, "issue":"required"} for attr, val in schema.__dict__.items() if not val], #Retorna o atributo na lista de atributos e valores se o valor não existir
            path=path
        )

class SemPermissao(ExceptionHTTP):
    def __init__(self, path):
        super().__init__(
            code=403,
            error='NÃO AUTORIZADO',
            message='Seu acesso não tem permissão para verificar este conteúdo! Entre em contato com a equipe técnica!',
            detail=[
                {'field':'cargo' if 'usuario' in path else 'cliente', 'issue': 'not authorized'}
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

