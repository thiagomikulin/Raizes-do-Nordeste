from Domain.__exceptions__ import EstoqueInsuficiente
from Infrastructure.Models.Empresa.mEstoque import Estoque
from Infrastructure.Models.Empresa.mFilial import Filial
from Infrastructure.Models.Empresa.mEstoqueItens import EstoqueItens
from Infrastructure.Models.Item.mIngrediente import Ingrediente
from Infrastructure.Models.Conectores.mItemReceita import ItemReceita
from Infrastructure.Models.Item.mVariacao import Variacao
from Infrastructure.Models.Vendas.mPedidoItens import ItensPed
from Infrastructure.Repositories.base import Session

def consultar_quantidade_estoque(pedido, sessao: Session):
    #Busca geral dos itens de estoque baseados nos itens
    filial = sessao.query(Filial).filter(Filial.id == pedido.filial).first()
    print('aqui')
    print(filial.estoque)

    print('teste')
    for estoque in filial.estoque:
        estoque = sessao.query(Estoque).filter(Estoque.id == estoque.id)
    for item in pedido.itens:
        retorno_quant = consultar_quantidade_estoque_individual(item.variacao, estoque, sessao)
        print(retorno_quant)
        for chave, valor in retorno_quant['receita'].items():
            quantidade_ingrediente = retorno_quant['receita'][chave]['quantidade_unidade']
            print(quantidade_ingrediente)
            print(item.quantidade)
            if  quantidade_ingrediente < item.quantidade:
                raise EstoqueInsuficiente(item)
            

    
def consultar_quantidade_estoque_individual(id_variacao: int, id_estoque:int, sessao: Session):

    #Busca geral dos itens de estoque baseados nos itens
    print(id_variacao)
    variacao = sessao.query(Variacao).filter(Variacao.id == id_variacao).first()
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

    for variacao, item_receita, ingrediente, estoque in variacao_nova:
        print(ingrediente.nome)
        print(item_receita.quantidade)
        print(estoque.quantidade)

    #Cálculo
    receita_geral = {}
    for variacao, item_receita, ingrediente, estoque in variacao_nova:
        nome = ingrediente.nome
        quantidade_necessaria = item_receita.quantidade
        quantidade_estoque = estoque.quantidade
        total_item =  quantidade_estoque // quantidade_necessaria
        receita_geral[nome] = {'quantidade da receita':f'{quantidade_necessaria} {item_receita.unidade_medida}', 'quantidade no estoque':f'{quantidade_estoque} {estoque.unidade_medida}', 'quantidade_unidade':total_item}
        print(receita_geral)
    

    return {
        'id':variacao.id,
        'nome':variacao.nome,
        'receita':receita_geral,
    }

        #EstoqueItens