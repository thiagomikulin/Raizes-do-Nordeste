from API.Routes.base import *
from Infrastructure.Repositories.base import Session, Depends, criar_sessao
from Application.base import verificar_token, verificar_permissao

#Recursos Variação
from API.Schemas.Itens.sVariacoes import CriacaoSchema
from Application.Item.fVariacao import verificar_schema_criacao_variacao


#Logs
from Infrastructure.Repositories.Registros.reLogs import salvar_log_bd

#exceptions
from Domain.exceptions import ExceptionHTTP, ExceptionGenerica

variacao_router = APIRouter(prefix='/variacoes', tags=['variacao'])

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Criar
@variacao_router.post('/criar')
async def criar_variacao(schema: CriacaoSchema, sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        verificar_schema_criacao_variacao(schema)
        verificar_permissao(ator, 'variação', 'criar')
        verificar_variacao_existe(schema.nome, sessao)
        variacao = criar_variacao_bd(schema, sessao)
        salvar_log_bd('criar','variacao','id',variacao['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return 

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Visualizar

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Editar
@variacao_router.put('/{id}')
async def editar_variacao(sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        salvar_log_bd('criar','variacao','id',variacao['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return 

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Ativar
@variacao_router.patch('/{id}/ativar')
async def ativar_variacao(sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        salvar_log_bd('criar','variacao','id',variacao['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return 

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Desativar
@variacao_router.patch('/{id}/desativar')
async def desativar_variacao(sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        salvar_log_bd('criar','variacao','id',variacao['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return 


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Adicionar item Receita
@variacao_router.put('/{id}/receita/{id_ingrediente}/adicionar')
async def alterar_receita(sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        salvar_log_bd('criar','variacao','id',variacao['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return 

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Remover item Receita
@variacao_router.put('/{id}/receita/{id_ingrediente}/remover')
async def alterar_receita(sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        salvar_log_bd('criar','variacao','id',variacao['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return 

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Associar com filial
@variacao_router.post('/{id}/filial/{id_filial}')
async def criar_variacao_filial(sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        salvar_log_bd('criar','variacao','id',variacao['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return 

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Desassociar com filial
@variacao_router.delete('/{id}/filial/{id_filial}')
async def apagar_variacao_filial(sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        salvar_log_bd('criar','variacao','id',variacao['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return 

