from API.Routes.base import APIRouter
from Application.base import verificar_token, verificar_permissao
from Infrastructure.Repositories.base import Session, Depends, criar_sessao


from API.Schemas.Pedido.sPedido import *

from Application.Vendas.fPedido import verificar_pedido_schema_criar,verificar_pedido_schema_editar , verificar_tipo_pedido, verificar_dono_pedido, progredir_status

from Infrastructure.Repositories.Vendas.rePedido import criar_pedido_bd, pedido_existe
from Infrastructure.Repositories.Persona.reCliente import cliente_existe
from Infrastructure.Repositories.Registros.reLogs import salvar_log_bd

from Domain.exceptions import SchemaExcept, SchemaInvalido, PermissionExcept, SemPermissao, MandatoryForFillingExcept, CamposObrigatorios, NotFoundExcept, NaoEncontrado

pedido_router = APIRouter(prefix='/pedidos', tags=['pedido'])

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Criar
@pedido_router.post('/criar')
async def criar_pedido(schema: CriacaoSchema, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    """
    Cria um novo pedido a partir dos dados passados
    """
    path='/pedidos/criar'
    try:
        verificar_pedido_schema_criar(schema)
        verificar_permissao(ator, 'pedido', 'criar')
        #Pode verificar também se o usuário (se for usuário) é um trabalhador da mesma filial que o pedido. Se não for, deve impedir a criação (implementação futura)
        verificar_tipo_pedido(schema) #consistência de mesas, clientes e entregas
        cliente_existe(schema.cliente, sessao)
        pedido = criar_pedido_bd(schema, sessao, ator)
        salvar_log_bd('criar','pedidos','id',pedido['pedido']['id'], ator, sessao)
    except SchemaExcept:
        raise SchemaInvalido(schema, path)
    except PermissionExcept:
        raise SemPermissao(path, ator)
    except MandatoryForFillingExcept as e:
        raise CamposObrigatorios(e.campos, path)
    except NotFoundExcept as e:
        raise NaoEncontrado(path, e.campos)
    else:
        return pedido

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Editar
@pedido_router.put('/{id}/editar')
async def editar_pedido(id:int, schema: EdicaoSchema, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    path = f'/pedidos/{id}/editar'
    try:
        verificar_pedido_schema_editar(schema)
        verificar_permissao(ator, 'pedido', 'editar')
    except SchemaExcept:
        raise SchemaInvalido(schema, path)

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# AtualizarStatus
@pedido_router.patch('/status/{id}')
async def atualizar_status_pedido(id: int, sessao: Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    path = f'/pedidos/status/{id}'
    try:
        pedido = pedido_existe(id, sessao) #verifica se o pedido existe
        verificar_permissao(ator, 'pedido', 'atualizar_status') #verifica se o ator pode criar
        verificar_dono_pedido(ator, pedido) #verifica se o ator é cliente e se for, se o pedido é dele
        pedido_update = progredir_status(pedido, sessao) #atualiza o status do pedido manualmente
    except NotFoundExcept as e:
        raise NaoEncontrado(path, e.campos)
    else:
        return pedido_update
    



#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Consultar

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Cancelar

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Itens - Adicionar

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Itens - Remover

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Itens - Editar

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Itens - Consultar



