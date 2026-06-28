#Bases
from API.Routes.base import *
from Application.base import *
from API.Schemas.Conectores.sPromoFilial import sPromoFilialCriacao, sPromoFilialExclusao
from Infrastructure.Models.Empresa.mFilial import Filial
from Infrastructure.Models.Conectores.mPromoFilial import PromoFilial
from Infrastructure.Repositories.base import criar_sessao, Session, Depends

from Application.chamada_rota import ativar_entidade, criar_entidade, desativar_entidade, editar_entidade, excluir_entidade, visualizar_entidade

#Exceptions
from Domain.__exceptions__ import ExceptionHTTP, ExceptionGenerica

#Complementares
from Infrastructure.Models.Vendas.mPedido import Pedido, StatusCode, TiposPed, CanalPedido, TipoLogin, FormaPagamento

#Requisitos
from API.Schemas.Empresa.sFilial import CriacaoSchema, EdicaoSchema
from Infrastructure.Repositories.Empresa.reFilial import criar_estoque_vinculado


filial_router = APIRouter(prefix='/filiais', tags=['Empresa - Filiais'])

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Filial - Criar (RF-F01)
@filial_router.post('/criar', status_code=201)
async def criar_filial(schema: CriacaoSchema, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        filial = criar_entidade(Filial, schema, ator, sessao, lista_regras_pos=[criar_estoque_vinculado])
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    return filial

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Atualizar
@filial_router.put('/{id}/atualizar')
async def atualizar_filial(id: int, schema: EdicaoSchema, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        filial_alterada = editar_entidade(id, Filial, schema, ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return filial_alterada

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Listar
@filial_router.get('/')
async def listar_filial(
    id: int | None = None, 
    cidade: str | None=None,
    estrutura: str | None=None,
    endereco: str | None=None,
    ativo: bool | None=None,
    sessao:Session = Depends(criar_sessao), 
    ator=Depends(verificar_token)
):
    dict_campos = {
        'id':id,
        'cidade':cidade,
        'estrutura':estrutura,
        'endereco':endereco,
        'ativo':ativo
    }
    try:
        lista = visualizar_entidade(Filial, sessao, ator, dict_campos)
        # verificar_permissao(ator, 'filial', 'listar')
        # lista = exec_busca(id, cidade, estrutura, endereco, ativo, sessao, ator)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return lista

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Ativar
@filial_router.patch('/{id}/ativar')
async def ativar_filial(id: int, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        #Adicionar regra complementar de ativar estoque junto
        filial_ativa = ativar_entidade(Filial, ator, id, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return filial_ativa


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Desativar
@filial_router.patch('/{id}/desativar')
async def desativar_filial(id: int, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        #Adicionar regra complementar de desativar estoque junto
        filial_desativa = desativar_entidade(Filial, ator, id, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return filial_desativa


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Consultar Vendas
@filial_router.get('/{id}/vendas')
async def consultar_vendas_filial(
    id: int | None = None, 
    status: StatusCode | None=None,
    tipo: TiposPed | None = None,
    canal: CanalPedido | None=None,
    tipo_criador: TipoLogin | None=None,
    id_criador: int | None=None,
    cliente: int | None=None,
    tipo_modificador: TipoLogin | None=None,
    id_modificador:int | None=None,
    forma_pagamento: FormaPagamento | None=None,
    sessao:Session = Depends(criar_sessao), 
    ator=Depends(verificar_token)
    ):
    dict_campos = {
        "filial":id, 
        "status":status, 
        "tipo":tipo, 
        "canal":canal, 
        "tipo_criador":tipo_criador, 
        "id_criador":id_criador, 
        "cliente":cliente, 
        "tipo_modificador":tipo_modificador, 
        "id_modificador":id_modificador, 
        "forma_pagamento":forma_pagamento, 
    }
    #OBS: usa método de busca padrão (mesma permissão de busca)
    try:
        lista = visualizar_entidade(Pedido, sessao, lista_campos=dict_campos, ator=ator)
        # verificar_permissao(ator, 'filial', 'listar vendas')
        # verificar_filial_existe(id, sessao)
        # lista = consultar_pedido(filial=id, sessao=sessao, ator=ator)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return lista


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Associar Campanhas
@filial_router.post('/{id}/campanha/{id_campanha}/associar', status_code=201)
async def associar_filial_campanha(id: int, id_campanha: int, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    schema = sPromoFilialCriacao(promocao=id_campanha, filial=id)
    try:
        relacao_criada = criar_entidade(PromoFilial, schema, ator, sessao, ['promocao', 'filial'])
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return relacao_criada


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Desassociar campanhas
@filial_router.delete('/{id}/campanha/{id_campanha}/desassociar')
async def desassociar_filial_campanha(id: int, id_campanha: int, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    schema = sPromoFilialExclusao(**{'filial':id, 'promocao':id_campanha})
    try:
        relacao_desfeita = excluir_entidade(PromoFilial, schema, ator, sessao, campo_verificacao=['filial','promocao'])
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return relacao_desfeita


