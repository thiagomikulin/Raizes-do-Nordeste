#Bases
from API.Routes.base import *
from Infrastructure.Repositories.base import Session, Depends, criar_sessao
from Application.base import verificar_permissao, verificar_token

from Application.chamada_rota import criar_entidade

#Exceptions
from Domain.__exceptions__ import ExceptionGenerica, ExceptionHTTP

#Logs
from Infrastructure.Repositories.Registros.reLogs import salvar_log_bd



#Requisitos 
from API.Schemas.Empresa.sCampanhaPromo import CriacaoSchema, EdicaoSchema
from Application.Empresa.fCampanhaPromo import verificar_schema_criacao_campanha, verificar_schema_edicao_campanha, verificar_alteracao_campanha, exec_busca
from Infrastructure.Repositories.Empresa.reCampanhaPromo import verificar_campanha_existe, criar_campanha_bd, editar_campanha_bd, ativar_campanhapromo_bd, desativar_campanhapromo_bd
from Infrastructure.Models.Empresa.mCampanhaPromo import CampanhaPromo

#Conectores
from Infrastructure.Repositories.Conectores.reUsuarioFilial import vincular_filial_bd, desvincular_filial_bd, verificar_vinculo_filial

#Complementares
from Infrastructure.Repositories.Empresa.reFilial import verificar_filial_existe

campanha_router = APIRouter(prefix='/campanhas', tags=['Empresa - Campanha']) #organizar por pasta pai pode ser interessante


# Criar
@campanha_router.post('/criar')
async def criar_campanha(schema: CriacaoSchema, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        campanha = criar_entidade(CampanhaPromo, schema, sessao, campo_verificacao=['nome'], ator=ator)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return campanha

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Consultar
@campanha_router.get('/')
async def buscar_campanha(
    id:int | None = None, 
    nome:str | None=None,
    desconto: int | None = None,
    validade: str | None = None,
    ativo: bool | None = None,
    filial:  int | None = None,
    sessao:Session = Depends(criar_sessao), 
    ator=Depends(verificar_token)):
    try:
        verificar_permissao(ator, 'campanha', 'consultar')
        lista = exec_busca(id, nome, desconto, validade, ativo, filial, sessao, ator)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return lista


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Editar
@campanha_router.put('/{id}')
async def editar_campanha(schema: EdicaoSchema, id: int,  sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        verificar_schema_edicao_campanha(schema)
        verificar_permissao(ator, 'campanha', 'editar')
        campanha = verificar_campanha_existe(id, sessao)
        campos = verificar_alteracao_campanha(schema, campanha)
        campanha_edit = editar_campanha_bd(schema, sessao)
        salvar_log_bd('editar','campanha',campos,campanha['campanha'], ator, sessao) #VERIFICAR
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return campanha_edit

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Ativar
@campanha_router.patch('/{id}/ativar')
async def ativar_campanhapromo(id: int, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        verificar_permissao(ator, 'campanha', 'ativar')
        campanha = verificar_campanha_existe(id, sessao)
        campanha_ativa = ativar_campanhapromo_bd(campanha, sessao)
        salvar_log_bd('ativar','campanha','ativo',campanha_ativa['campanha']['ativo'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return campanha_ativa

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Desativar
@campanha_router.patch('/{id}/desativar')
async def desativar_campanhapromo(sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        verificar_permissao(ator, 'campanha', 'desativar')
        campanha = verificar_campanha_existe(id, sessao)
        campanha_desativa = desativar_campanhapromo_bd(campanha, sessao)
        salvar_log_bd('desativar','campanha','ativo',campanha_desativa['campanha']['ativo'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return campanha_desativa

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Vincular Filial (UsuarioFilial)
@campanha_router.post('/{id}/filial/{id_filial}/vincular')
async def vincular_filial(id: int, id_filial: int, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        verificar_permissao(ator, 'campanha', 'vincular')
        campanha = verificar_campanha_existe(id, sessao)
        filial = verificar_filial_existe(id_filial, sessao)
        vinculo = verificar_vinculo_filial(campanha.id, filial.id, sessao)
        cria_vinculo = vincular_filial_bd(campanha.id, filial.id, vinculo,  sessao)
        salvar_log_bd('criar','usuarioFilial','id',vinculo['id'], ator, sessao) #verificar alteração para dict
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return cria_vinculo

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Desvincular Filial (UsuarioFilial)
@campanha_router.delete('/{id}/filial/{id_filial}/desvincular')
async def desvincular_filial(id: int, id_filial: int, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        verificar_permissao(ator, 'campanha', 'vincular')
        campanha = verificar_campanha_existe(id, sessao)
        filial = verificar_filial_existe(id_filial, sessao)
        vinculo = verificar_vinculo_filial(campanha.id, filial.id, sessao)
        quebra_vinculo = desvincular_filial_bd(campanha.id, filial.id, vinculo, sessao)
        salvar_log_bd('excluir','usuarioFilial','id',quebra_vinculo[''], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return quebra_vinculo


