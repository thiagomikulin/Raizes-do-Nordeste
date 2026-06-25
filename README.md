# Raízes do Nordeste

Este projeto foi desenvolvido com a premissa de gerenciar vendas, estoque e demais recursos para a rede de restaurantes "Raízes do Nordeste"

# Requisitos do projeto

Para que o projeto possa rodar localmente em sua máquina, é necessário ter instalado:
* Docker <https://docs.docker.com/get-started/get-docker/> (versão 29.1.3)
  * Necessário para isolar a API do seu sistema operacional, evitando portanto erros de conflito de importação com seu sistema operacional
* Docker compose <https://docs.docker.com/compose/install> (versão 1.29.2)
  * necessário para operacionalizar tanto o banco de dados quanto a aplicação simultaneamente, em ambientes separados, mas integrados
* Para sistemas Windows --> Docker Desktop
  * necessário para rodar o servidor a partir de máquinas Windows (comandos com script não funcionam em máquinas Windows)
  *  O docker precisará também ter o Windows Subserver for Linux para rodar o Docker. Geralmente, é instalado junto ao docker, mas pode ser necessário reiniciar o sistema.
  * Pode ser utilizado também para sistemas Linux opcionalmente (o projeto já vem com um script executável para Linux)

## Aplicações usadas:

* Python 3.13
  * Todas as dependências do Python encontram-se no caminho '/Infrastructure/requirements.txt'
* MySQL (instalado automaticamente através da imagem)

# Como rodar o projeto

Para rodar o projeto, é necessário importar todo o código para dentro de sua máquina

1. Baixe o .zip do projeto (clicando em code, no topo desta aba, ou seguindo este link: https://github.com/thiagomikulin/Raizes-do-Nordeste/archive/refs/heads/main.zip)
2. Escolha uma pasta onde deseja armazenar o servidor
3. Extraia o arquivo zip nesta pasta
4. Na pasta do projeto, edite o arquivo ".env.example" e preencha conforme o padrão:
   1. DB_USER = user
   2. DB_PASSWORD = password
   3. DB_DATABASE = raizes_do_nordeste
   4. DB_PORT=3307 (se não tiver outro sql rodando, pode alterar para a 3306)
   5. SECRET_KEY=sua_chave
   6. SECRET_KEY_REFRESH=chave_refresh
   7. ALGORITHM=HS256
   8. EMAIL_HOST=seu_email (para envio de email de reset de senha)
   9. EMAIL_PW=senhaemail (para envio de email de reset de senha)
      1. Esta senha pode ser gerada pela conta do google também (seguindo este tutorial: https://support.google.com/wallet/answer/2461835?hl=pt-BR)
   10. ACCESS_TOKEN_EXPIRE_MINUTES=30
      1. OBS: não será necessário copiar os arquivos manualmente para o env. A execução das próximas etapas fará esse processo automaticamente.
5.  Para sistemas Windows
    1.  Abra o Docker Desktop
    2.  Na pasta do projeto, abra o terminal
    3.  Rode os seguintes comandos
    4.  copy .env.example .env
    5.  docker-compose up --build
    6.  A partir deste ponto, você poderá visualizar o containter e a operação deste através do terminal do Docker Desktop 
6.  Para sistemas Linux
   1. Altere a permissão de execução do arquivo "run_server.sh" para permitir execução
   2. Clique no run_server.sh (obs: selecione a opção de executar pelo terminal)
      1. Este script executa o compose up do container
      2. Caso o script não funcione, executar no terminal a partir da pasta do projeto:
         1. cp .env.example .env
         2. docker-compose up --build
         3. Para encerrar após o uso:
            1. Ctrl+C
            2. docker-compose down
    3.  Após algum tempo, no terminal, exibirá uma mensagem de que a aplicação está rodando pela URL "http://localhost:8000/docs".
7.  Acesse a URL "http://localhost:8000/docs" e você poderá ver o servidor funcionando!
    1.  Em sistemas Linux, caso queira encerrar o servidor após o uso, basta voltar ao terminal aberto e apertar Ctrl+C
        1.  Este processo deverá encerrar automaticamente instâncias abertas do docker-compose, persistindo o banco de dados

Através dos comandos Docker, tanto a aplicação quanto o banco de dados devem rodar localmente em sua máquina.
Caso queira visualizar o banco de dados, precisará ser criada uma conexão com este (OBS: para a elaboração do guia a seguir, foi utilizado como base de referência o SGBD dBeaver):

1. Crie uma nova conexão
2. Selecione a opção de conectar a um banco MySQL
3. Selecione conexão de host
4. Preenchimento de campos:
   1. Server Host: mysql
   2. Port: porta definida no .env.example
   3. Database: db definido no .env.example
   4. Username: usuario definido no .env.example
   5. Password: senha definida no .env.example
5. Teste a conexão.
   1. Caso retorne algum erro de chave pública, edite nas propriedades de Driver do seu SGBD selecionado
6. Após testar, pode confirmar e começar a utilizar!
   1. Crie um novo script clicando com o botão direito sobre a conexão, e selecione SQL Editor --> Open SQL Script

As tabelas são conforme se segue:
* campanhaPromos
* clientes
* estoqueItens
* estoques
* filiais
* filiaisPromos
* ingredientes
* logs
* movimentoItens
* movimentos
* pedidoItens
* pedidos
* produtos
* receitasItens
* usuarios
* usuariosFiliais
* variacoes
* variacoesFiliais

Para consulta de cada uma das tabelas, utilize métodos SQL correspondentes

# Testes no projeto 

Após colocar o servidor no ar, os testes poderão ser realizados por 2 meios:
* URL http://localhost:8000/docs (documentação padrão da FastAPI em Swagger, com todos os PATHs)
* Collection com os testes realizados durante a implementação (que poderão ser baixada através do link: <>)

# Implementações futuras

Esta parte da fundamentação se dedica a estruturar como manter o suporte ao sistema futuramente.

## Migrações no projeto

Quaisquer implementações adicionais ou alterações no banco de dados deverão seguir as seguintes etapas:
1. Alterar o arquivo de modelo, localizado na página Infrastructure/Models/Setor/Tabela
2. Após realizar a alteração, na pasta do projeto no terminal, executar:  alembic -c Infrastructure/alembic.ini revision --autogenerate -m "Mensagem"
   1. Se retornar algum erro, verificar pelo código e arquivo. As mensagens costumam indicar a origem do erro pelo próprio arquivo
3. Depois de enviado o versionamento da modelagem, executar o comando: alembic -c Infrastructure/alembic.ini upgrade head
   1. Caso retorne algum erro nesta etapa, será necessário excluir o versionamento anterior enviado. Os versionamentos ficam armazenados em: Infrastructure/alembic/versions (é possível identificar pela mensagem)
