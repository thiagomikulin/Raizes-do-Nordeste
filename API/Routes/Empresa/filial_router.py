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

from Domain.exceptions import SchemaExcept, SchemaInvalido, PermissionExcept, SemPermissao, ConflictExcept, Conflito

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
    except SchemaExcept:
        raise SchemaInvalido(schema, path)
    except PermissionExcept:
        raise SemPermissao(path, ator)
    except ConflictExcept:
        raise Conflito('Filial', 'conta', schema.conta_banc, path)
    return filial

    

# Atualizar

# Listar

# Ativar

# Desativar

# Consultar Vendas

# Associar Campanhas

# Desassociar campanhas

