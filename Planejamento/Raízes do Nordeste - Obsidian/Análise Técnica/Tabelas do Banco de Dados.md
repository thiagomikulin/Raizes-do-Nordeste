
# Usuários

## Campos

* ID
* Nome
* Cargo
	* Gerente
	* Cozinheiro
	* Atendente
	* Não categorizado
	* TI (eu)
* Login
* Senha
* Tipo_user
	* Pessoa
	* Totem
	* App
		* App próprio
		* iFood

## Permissões funcionais

* X Criação de usuários
	* Gerentes
		* Tudo, menos gerentes
	* TI
* Visualização de usuários
	* Gerentes
	* TI
* Atualização de usuários
	* Gerentes
		* Tudo, menos gerentes
	* TI
* Delete
	* Apenas TI



# Clientes

## Campos

* ID
* Nome
* E-mail/CPF
* Reconhecimento Facial(?) /senha
* Endereço
* Fidelidade

## Permissões funcionais

* Criação de clientes
	* Gerentes
	* Atendentes
	* TI
* Leitura de clientes
	* Gerentes
	* Atendentes
	* TI
* Atualização de clientes
	* Gerentes
	* TI
* Delete clientes
	* Apenas TI

# Filiais

## Campos

* ID
* Nome
* Endereço

# Pedidos

## Campos

* ID
* Filial
* Status
* Usuário
	* Quem criou o pedido
* Cliente
* Mesa (opcional)

## Permissões funcionais

* Criação de pedidos
	* Gerentes
	* Atendentes
	* TI
* Leitura de pedidos
	* Gerentes
	* Atendentes
	* Cozinheiros
	* TI
* Atualização de pedidos
	* Gerentes
	* Atendentes
	* Cozinheiros
		* Apenas status --> aguardando coleta
* Delete pedido
	* Apenas TI

# PedItens

## Campos

* ID
* Produto
* Status
* Pedido

## Permissões funcionais

* Adição de itens
	* Gerentes
	* Atendentes
	* TI
* Leitura de itens
	* Gerentes
	* Atendentes
	* Cozinheiros
	* TI
* Atualização de itens
	* Gerentes
	* Atendentes
	* Cozinheiros
		* Apenas status
	* TI
* Delete itens
	* Gerentes
	* Atendentes
	* TI


# Produtos

## Campos

* ID
* Nome
* Filial

## Permissões funcionais

Estes processos serão de exclusividade do TI, pois se colocar essa autorização para um gerente que seja, primeiro teria que passar pela dona da rede, que teria que aprovar a criação destes produtos. (AUDITORIA de criação e avaliação de possibilidades)
* Criação de produtos
	* TI
* Deletar produtos
	* TI

# Logs

## Campos

* ID
* Data
* Usuário
* Tabela
* Ação

# UsuárioFilial

# Variações

Campos

* ID
* IdProduto
* IdFilial

# Ingredientes

