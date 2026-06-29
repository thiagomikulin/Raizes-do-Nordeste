from Infrastructure.Models.Vendas.mPedido import Pedido
from Domain.__exceptions__ import EstoqueInsuficiente
from Infrastructure.Models.Empresa.mEstoque import Estoque
from Infrastructure.Models.Empresa.mFilial import Filial
from Infrastructure.Models.Empresa.mEstoqueItens import EstoqueItens
from Infrastructure.Models.Item.mIngrediente import Ingrediente
from Infrastructure.Models.Conectores.mItemReceita import ItemReceita
from Infrastructure.Models.Item.mVariacao import Variacao
from Infrastructure.Models.Vendas.mPedidoItens import ItensPed
from Infrastructure.Repositories.base import Session

#Objetivo - indicar se há estoque suficiente de todos os itens (a consulta utilizada é a mesma do endpoint de consultar quantia de estoque)
def consultar_quantidade_estoque(pedido, sessao: Session):

    #Busca geral dos itens de estoque baseados nos itens
    filial = sessao.query(Filial).filter(Filial.id == pedido.filial).first()
    for estoque in filial.estoque:
        estoque = sessao.query(Estoque).filter(Estoque.id == estoque.id)
    for item in pedido.itens:
        retorno_quant = consultar_quantidade_estoque_individual(item.variacao, estoque, sessao)
        for chave, valor in retorno_quant['receita'].items():
            quantidade_ingrediente = retorno_quant['receita'][chave]['quantidade_unidade']
            if  quantidade_ingrediente < item.quantidade:
                raise EstoqueInsuficiente(item)
            
def consultar_quantidade_estoque_item(item, sessao: Session):
    item_ped = sessao.query(ItensPed).filter(ItensPed.id == item.id).first()
    pedido = sessao.query(Pedido).filter(Pedido.id == item_ped.id_ped).first()
    print('tem pedido')
    filial = sessao.query(Filial).filter(Filial.id == pedido.filial).first()
    print('tem filial')
    retorno_quant = consultar_quantidade_estoque_individual(item.variacao, filial.estoque, sessao)
    for chave, valor in retorno_quant['receita'].items():
            quantidade_ingrediente = retorno_quant['receita'][chave]['quantidade_unidade']
            if  quantidade_ingrediente < item.quantidade:
                raise EstoqueInsuficiente(item)
            
def consultar_quantidade_estoque_variacao(variacao, sessao: Session):
    variacao_estoque = sessao.query(Variacao).filter(Variacao.id == variacao.variacao).first()
    pedido = sessao.query(Pedido).filter(Pedido.id == variacao.id_ped).first()
    print('tem pedido')
    filial = sessao.query(Filial).filter(Filial.id == pedido.filial).first()
    print('tem filial')
    retorno_quant = consultar_quantidade_estoque_individual(variacao_estoque.id, filial.estoque, sessao)
    print('saiu daqui')
    print(retorno_quant)
    for chave, valor in retorno_quant['receita'].items():
            quantidade_ingrediente = retorno_quant['receita'][chave]['quantidade_unidade']
            print('quantidade ingrediente',quantidade_ingrediente)
            print('quantidade solicitada',variacao.quantidade)
            if  quantidade_ingrediente < variacao.quantidade:
                raise EstoqueInsuficiente(variacao_estoque)
    
def consultar_quantidade_estoque_individual(id_variacao: int, id_estoque:int, sessao: Session):

    #Busca geral dos itens de estoque baseados nos itens
    variacao = sessao.query(Variacao).filter(Variacao.id == id_variacao).first()
    print('tem variação')
    variacao_nova = sessao.query(Variacao, ItemReceita, Ingrediente, EstoqueItens).select_from(
        Variacao
    ).join(
        ItemReceita,
        ItemReceita.variacao == Variacao.id 
    ).join(
        Ingrediente,
        Ingrediente.id == ItemReceita.ingrediente
    ).join(
        EstoqueItens,
        EstoqueItens.ingrediente == Ingrediente.id and EstoqueItens.estoque == id_estoque
    ).filter(Variacao.id == id_variacao).all()

    # for variacao, item_receita, ingrediente, estoque in variacao_nova:
    #     print(ingrediente.nome)
    #     print(item_receita.quantidade)
    #     print(estoque.quantidade)

    #Cálculo
    receita_geral = {}
    for variacao, item_receita, ingrediente, estoque in variacao_nova:
        nome = ingrediente.nome
        quantidade_necessaria = item_receita.quantidade
        quantidade_estoque = estoque.quantidade
        total_item =  quantidade_estoque // quantidade_necessaria
        receita_geral[nome] = {'quantidade da receita':f'{quantidade_necessaria} {item_receita.unidade_medida}', 'quantidade no estoque':f'{quantidade_estoque} {estoque.unidade_medida}', 'quantidade_unidade':total_item}
    

    return {
        'id':variacao.id,
        'nome':variacao.nome,
        'receita':receita_geral,
    }

        #EstoqueItens