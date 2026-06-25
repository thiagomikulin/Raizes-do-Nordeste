from API.Routes.base import *
from API.Schemas.Conectores.sVariacaoFilial import sVariacaoFilialCriacao, sVariacaoFilialExclusao
from Infrastructure.Repositories.base import Session, Depends, criar_sessao
from Application.base import verificar_token, verificar_permissao

from Application.chamada_rota import ativar_entidade, criar_entidade, desativar_entidade, editar_entidade, excluir_entidade, visualizar_entidade

#Recursos Variação
from API.Schemas.Itens.sVariacoes import CriacaoSchema, EdicaoSchema
from API.Schemas.Conectores.sItemReceita import InternoReceitaCriacaoSchema, InternoReceitaEdicaoSchema, ReceitaCriacaoSchema, ReceitaExclusaoSchema, ReceitaEdicaoSchema
from Infrastructure.Models.Item.mVariacao import Variacao
from Infrastructure.Models.Conectores.mItemReceita import ItemReceita
from Infrastructure.Models.Conectores.mVariacaoFilial import VariacaoFilial

#Logs
from Infrastructure.Repositories.Registros.reLogs import salvar_log_bd

#exceptions
from Domain.__exceptions__ import Conflito, ExceptionHTTP, ExceptionGenerica

variacao_router = APIRouter(prefix='/variacoes', tags=['Itens - Variações'])

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Criar
@variacao_router.post('/criar')
async def criar_variacao(schema: CriacaoSchema, sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        variacao = criar_entidade(Variacao, schema, ator, sessao, campo_verificacao=['nome'])
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return variacao

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Visualizar
@variacao_router.get('/')
async def buscar_variacao(
    id: int | None=None,
    nome:str | None=None,
    produto: int | None=None,
    preco_unitario: float | None=None,
    ativo:bool | None=None,
    sessao:Session = Depends(criar_sessao), 
    ator=Depends(verificar_token)
):
    dict_campos = {
        "id":id,
        "nome":nome,
        "produto":produto,
        "preco_unitario":preco_unitario,
        "ativo":ativo
    }
    try:
        lista = visualizar_entidade(Variacao, sessao, ator, dict_campos)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    return lista

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Editar
@variacao_router.put('/{id}/editar')
async def editar_variacao(id: int, schema: EdicaoSchema, sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        variacao_editada = editar_entidade(id, Variacao, schema, ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return variacao_editada

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Ativar
@variacao_router.patch('/{id}/ativar')
async def ativar_variacao(id: int, sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        variacao_ativa = ativar_entidade(Variacao, ator, id, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return variacao_ativa

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Desativar
@variacao_router.patch('/{id}/desativar')
async def desativar_variacao(id: int, sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    try:
        variacao_desativa = desativar_entidade(Variacao, ator, id, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return variacao_desativa


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Adicionar item Receita
@variacao_router.post('/{id_variacao}/receita/{id_ingrediente}/adicionar')
async def adicionar_item_receita(id_variacao: int, id_ingrediente: int, schema: ReceitaCriacaoSchema, sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    template = schema.model_dump()
    schema_interno = InternoReceitaCriacaoSchema(quantidade=template['quantidade'], unidade_medida=template['unidade_medida'],variacao=id_variacao, ingrediente=id_ingrediente)
    
    try:
        item_receita = criar_entidade(ItemReceita, schema_interno, ator, sessao, ['variacao', 'ingrediente'])
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return item_receita

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#Editar item Receita
@variacao_router.put('/{id_variacao}/receita/{id_ingrediente}/editar')
async def editar_item_receita(id_variacao: int, id_ingrediente: int, schema: ReceitaEdicaoSchema,sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    template = schema.model_dump()
    schema_interno = InternoReceitaEdicaoSchema(quantidade=template['quantidade'], unidade_medida=template['unidade_medida'],variacao=id_variacao, ingrediente=id_ingrediente)
    try:
        variacao_edietada = editar_entidade({'variacao':id_variacao, 'ingrediente':id_ingrediente}, ItemReceita, schema_interno, ator, sessao)
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica(e)
    else:
        return variacao_edietada

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Remover item Receita
@variacao_router.delete('/{id_variacao}/receita/{id_ingrediente}/remover')
async def remover_item_receita(id_variacao: int, id_ingrediente: int,sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    schema = ReceitaExclusaoSchema(ingrediente=id_ingrediente, variacao=id_variacao)
    try:
        variacao_excluida = excluir_entidade(ItemReceita, schema, ator, sessao, ['ingrediente', 'variacao'])
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return variacao_excluida

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Associar com filial
@variacao_router.post('/{id_variacao}/filial/{id_filial}/associar')
async def criar_variacao_filial(id_variacao: int, id_filial: int, sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    schema = sVariacaoFilialCriacao(variacao=id_variacao, filial=id_filial)
    try:
        variacao_filial_criada = criar_entidade(VariacaoFilial, schema, ator, sessao, ['variacao', 'filial'])
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return variacao_filial_criada

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Desassociar com filial
@variacao_router.delete('/{id_variacao}/filial/{id_filial}')
async def apagar_variacao_filial(id_variacao:int, id_filial: int, sessao: Session = Depends (criar_sessao), ator = Depends(verificar_token)):
    schema = sVariacaoFilialExclusao(variacao=id_variacao, filial=id_filial)
    try:
        variacao_filial_excluida = excluir_entidade(VariacaoFilial, schema, ator, sessao, ['variacao', 'filial'])
    except ExceptionHTTP:
        raise
    except Exception as e:
        raise ExceptionGenerica
    else:
        return variacao_filial_excluida

