from Infrastructure.Models.Empresa.mEstoqueItens import EstoqueItens
from Infrastructure.Models.Item.mIngrediente import Ingrediente
from Infrastructure.Models.Conectores.mItemReceita import ItemReceita
from Infrastructure.Models.Item.mVariacao import Variacao
from Infrastructure.Models.Vendas.mPedidoItens import ItensPed
from Infrastructure.Repositories.base import Session

def consultar_quantidade_estoque(pedido, sessao: Session):
    #Busca geral dos itens de estoque baseados nos itens
    for item in pedido.itens:
        variacao = sessao.query(Variacao).filter(Variacao.id == item.variacao).first()
        lista_receita = sessao.query(ItemReceita).filter(ItemReceita.variacao == variacao.id).all()
        lista_ingredientes = []
        for ingrediente in lista_receita:
            ingrediente = sessao.query(Ingrediente).filter(Ingrediente.id == ingrediente.id).first()
            lista_ingredientes.append(ingrediente)
        lista_itens_estoque = []
        for ingrediente in lista_ingredientes:
            item_estoque = sessao.query(EstoqueItens).filter(EstoqueItens.ingrediente == ingrediente.id).first()
            lista_itens_estoque.append(item_estoque)
    
    #Cálculo
    print(variacao)
    print(lista_receita)
    print(lista_ingredientes)
    print(lista_itens_estoque)
    
def consultar_quantidade_estoque_individual(id_variacao: int, id_estoque:int, sessao: Session):

    #Busca geral dos itens de estoque baseados nos itens
    print(id_variacao)
    variacao = sessao.query(Variacao).filter(Variacao.id == id_variacao).first()
    print(variacao)
    lista_receita = sessao.query(ItemReceita).filter(ItemReceita.variacao == variacao.id).all()
    lista_ingredientes = []
    for ingrediente in lista_receita:
        ingrediente = sessao.query(Ingrediente).filter(Ingrediente.id == ingrediente.ingrediente).first()
        lista_ingredientes.append(ingrediente)
    ingrediente_dict = {
        ingrediente.id:ingrediente.nome
        for ingrediente in lista_ingredientes
    }
    lista_itens_estoque = []
    for ingrediente in lista_ingredientes:
        item_estoque = sessao.query(EstoqueItens).filter(EstoqueItens.ingrediente == ingrediente.id and EstoqueItens.id == id_estoque).first()
        print(ingrediente.id)
        
        lista_itens_estoque.append(item_estoque)
    
    item_estoque_dict = {
        item.ingrediente:f'{item.quantidade} {item.unidade_medida}'
        for item in lista_itens_estoque
    }
    print(item_estoque_dict)

    #Cálculo
    receita_geral = {}
    for item in lista_receita:
        nome = ingrediente_dict.get(item.ingrediente)
        quant_estoque = item_estoque_dict.get(item.ingrediente)
        lista_quant = quant_estoque.split()
        total_item = int(lista_quant[0]) // item.quantidade
        receita_geral[nome] = {'quantidade':f'{item.quantidade} {item.unidade_medida}', 'quantidade_estoque':f'{quant_estoque}', 'quantidade_unidade':total_item}
    for item in receita_geral:
        print(item['quantidade_unidade'])
        total_variacao = 0
    

    return {
        'id':variacao.id,
        'nome':variacao.nome,
        'receita':receita_geral,
        'total':total_variacao
    }

        #EstoqueItens