#Bases
from datetime import date



from API.Routes.base import *
from Infrastructure.Repositories.base import Session, Depends, criar_sessao
from Application.base import verificar_token

#Application
from Application.chamada_rota import ativar_entidade, criar_entidade, desativar_entidade, editar_entidade, excluir_entidade, visualizar_entidade

#Exceptions
from Domain.__exceptions__ import ExceptionGenerica, ExceptionHTTP

#Requisitos 
from API.Schemas.Empresa.sCampanhaPromo import CriacaoSchema, EdicaoSchema
from API.Schemas.Conectores.sPromoFilial import sPromoFilialCriacao, sPromoFilialExclusao
from Infrastructure.Models.Empresa.mCampanhaPromo import CampanhaPromo
from Infrastructure.Models.Conectores.mPromoFilial import PromoFilial

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

campanha_router = APIRouter(prefix='/campanhas', tags=['Empresa - Campanhas']) #organizar por pasta pai pode ser interessante

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Criar
@campanha_router.post('/criar', status_code=201)
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
    validade: date | None = None,
    ativo: bool | None = None,
    sessao:Session = Depends(criar_sessao), 
    ator=Depends(verificar_token)):
    dict_campos = {
        'id':id,
        'nome':nome,
        'desconto':desconto,
        'validade':validade,
        'ativo':ativo
    }
    try:
        lista = visualizar_entidade(CampanhaPromo,sessao, ator, dict_campos)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return lista


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Editar
@campanha_router.put('/{id}/editar')
async def editar_campanha(schema: EdicaoSchema, id: int,  sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        campanha_edit = editar_entidade(id, CampanhaPromo, schema, ator, sessao)
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
        campanha_ativa = ativar_entidade(CampanhaPromo, ator, id, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return campanha_ativa

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Desativar
@campanha_router.patch('/{id}/desativar')
async def desativar_campanhapromo(id: int, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        campanha_desativa = desativar_entidade(CampanhaPromo, ator, id, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return campanha_desativa

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Vincular Filial (UsuarioFilial)
@campanha_router.post('/{id}/filial/{id_filial}/vincular', status_code=201)
async def vincular_filial(id: int, id_filial: int, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    schema = sPromoFilialCriacao(promocao=id, filial=id_filial)
    try:
        cria_vinculo = criar_entidade(PromoFilial, schema, ator, sessao, ['promocao', 'filial'])
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
    schema = sPromoFilialExclusao(promocao=id, filial=id_filial)
    try:
        quebra_vinculo = excluir_entidade(PromoFilial, schema, ator, sessao, ['filial','promocao'])
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return quebra_vinculo



