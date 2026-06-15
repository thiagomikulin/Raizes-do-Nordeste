from fastapi import APIRouter

pedido_router = APIRouter(prefix='/pedido', tags=['pedido'])

# Criar
@pedido_router.get('/criae')
async def criar_pedido():
    """
    Cria um novo pedido a partir dos dados passados
    """
    return {'pedido':1}

# Editar

# AtualizarStatus

# Consultar

# Cancelar

# Itens - Adicionar

# Itens - Remover

# Itens - Editar

# Itens - Consultar



