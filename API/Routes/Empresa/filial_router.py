#Bases
from API.Routes.base import *
from Application.base import *
from Infrastructure.Repositories.base import criar_sessao, Session, Depends

#API
from API.Schemas.Empresa.sFilial import *

#Application
from Application.Empresa.fFilial import verificar_schema_criacao

#Repositories
from Infrastructure.Repositories.Empresa.reFilial import verificar_filial_criacao, criar_filial_bd

from Domain.exceptions import ExceptionHTTP, ExceptionGenerica

from Infrastructure.Repositories.Registros.reLogs import salvar_log_bd

filial_router = APIRouter(prefix='/filiais', tags=['filial'])

#Criar
@filial_router.post('/criar')
async def criar_filial(schema: CriacaoSchema, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    path='/filiais/criar'
    try:
        verificar_schema_criacao(schema)
        verificar_permissao(ator, 'filial', 'criar')
        verificar_filial_criacao(schema.conta_banc, sessao)
        filial = criar_filial_bd(schema, sessao)
        salvar_log_bd('criar','filial','id',filial['filial']['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    return filial

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Atualizar
@filial_router.put('/{id}')
async def atualizar_filial():
    pass

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Listar
@filial_router.get('/')
async def listar_filial():
    pass

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Ativar
@filial_router.patch('/{id}/ativar')
async def ativar_filial():
    pass

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Desativar
@filial_router.patch('/{id}/desativar')
async def desativar_filial():
    pass

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Consultar Vendas
@filial_router.get('/vendas')
async def consultar_vendas_filial():
    pass

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Associar Campanhas
@filial_router.post('/{id}/campanha/associar/{id_campanha}')
async def associar_filial_campanha():
    pass

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Desassociar campanhas
@filial_router.post('/{id}/campanha/desassociar/{id_campanha}')
async def desassociar_filial_campanha():
    pass

