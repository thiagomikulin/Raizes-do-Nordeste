#Bases
from API.Routes.base import *
from Application.base import *
from Infrastructure.Repositories.base import criar_sessao, Session, Depends

from Application.chamada_rota import criar_entidade, visualizar_entidade

#Exceptions
from Domain.__exceptions__ import ExceptionHTTP, ExceptionGenerica
#Logs
from Infrastructure.Repositories.Registros.reLogs import salvar_log_bd

#Complementares
from Infrastructure.Models.Vendas.mPedido import Pedido, StatusCode, TiposPed, CanalPedido, TipoLogin, FormaPagamento

#Requisitos
from API.Schemas.Empresa.sFilial import CriacaoSchema, EdicaoSchema
from Application.Empresa.fFilial import verificar_schema_criacao, verificar_schema_edicao, exec_busca, verificar_alteracao
from Infrastructure.Repositories.Empresa.reFilial import verificar_filial_criacao, criar_filial_bd, verificar_filial_existe, desativar_filial_bd, ativar_filial_bd, atualizar_filial_db, criar_estoque_vinculado
from Infrastructure.Models.Empresa.mFilial import Filial

#Complementares
from Infrastructure.Repositories.Empresa.reCampanhaPromo import verificar_campanha_existe
from Infrastructure.Repositories.Conectores.reFiliaisPromo import verificar_vinculo_filial, associar_filial_campanha_db, desassociar_filial_campanha_db
from API.Routes.Pedido.pedido_router import consultar_pedido

filial_router = APIRouter(prefix='/filiais', tags=['empresa'])

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Filial - Criar (RF-F01)
@filial_router.post('/criar')
async def criar_filial(schema: CriacaoSchema, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        filial = criar_entidade(Filial, schema, ator, sessao, campo_verificacao=['conta_banc'], lista_regras_pos=[criar_estoque_vinculado])
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    return filial

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Atualizar
@filial_router.put('/{id}')
async def atualizar_filial(id: int, schema: EdicaoSchema, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        verificar_schema_edicao(schema)
        verificar_permissao(ator, 'filial', 'editar')
        filial = verificar_filial_existe(id, sessao)
        campos = verificar_alteracao(filial, schema)
        filial_alterada = atualizar_filial_db(schema, sessao)
        salvar_log_bd('criar','filial','id',filial_alterada['filial']['id'], ator, sessao)
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
        print(type(ator))
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
        verificar_permissao(ator, 'filial', 'ativar')
        verificar_filial_existe(id, sessao)
        filial_ativa = ativar_filial_bd(id, sessao)
        salvar_log_bd('ativar','filial','id',filial_ativa['id'], ator, sessao)
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
        verificar_permissao(ator, 'filial', 'ativar')
        verificar_filial_existe(id, sessao)
        filial_desativa = desativar_filial_bd(id, sessao)
        salvar_log_bd('desativar','filial','id',filial_desativa['id'], ator, sessao)
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
@filial_router.post('/{id}/campanha/{id_campanha}/associar')
async def associar_filial_campanha(id: int, id_campanha: int, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        verificar_permissao(ator, 'filial', 'associar') #O usuário tem permissão de associar campanha com filial?
        filial = verificar_filial_existe(id, sessao) #A filial passada pelo id é válida?
        campanha = verificar_campanha_existe(id_campanha, sessao) #A campanha passada pelo id é válida?
        relacao = verificar_vinculo_filial(filial.id, campanha.id, sessao) #O vínculo entre campanha e filial já existe?
        relacao_criada = associar_filial_campanha_db(filial.id, campanha.id, relacao, sessao) #Se o vínculo NÃO existir, retorna erro
        salvar_log_bd('criar','FilialPromo','id',relacao_criada['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return relacao_criada


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Desassociar campanhas
@filial_router.post('/{id}/campanha/desassociar/{id_campanha}')
async def desassociar_filial_campanha(id: int, id_campanha: int, sessao:Session = Depends(criar_sessao), ator=Depends(verificar_token)):
    try:
        verificar_permissao(ator, 'filial', 'associar') #O usuário tem permissão de associar campanha com filial?
        filial = verificar_filial_existe(id, sessao) #A filial passada pelo id é válida?
        campanha = verificar_campanha_existe(id_campanha, sessao) #A campanha passada pelo id é válida?
        relacao = verificar_vinculo_filial(filial.id, campanha.id, sessao) #O vínculo entre campanha e filial já existe?
        relacao_desfeita = desassociar_filial_campanha_db(filial.id, campanha.id, relacao, sessao) #Se o vínculo não existir, retorna erro
        salvar_log_bd('criar','FilialPromo','id',relacao_desfeita['id'], ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return relacao_desfeita


