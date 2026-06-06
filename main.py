from fastapi import FastAPI

app = FastAPI()

from API.Routes.pedido_router import pedido_router
from API.Routes.produto_router import produto_router

app.include_router(pedido_router)
app.include_router(produto_router)