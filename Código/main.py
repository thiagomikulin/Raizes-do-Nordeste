from fastapi import FastAPI

app = FastAPI()

from Routes.pedido_router import pedido_router
from Routes.produto_router import produto_router

app.include_router(pedido_router)
app.include_router(produto_router)