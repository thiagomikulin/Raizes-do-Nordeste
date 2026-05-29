from fastapi import FastAPI

app = FastAPI()

from Routes.pedido_router import pedido_router

app.include_router(pedido_router)