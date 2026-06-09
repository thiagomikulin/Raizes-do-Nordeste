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


    