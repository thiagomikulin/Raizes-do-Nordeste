# Raízes do Nordeste

Este projeto foi desenvolvido com a premissa de gerenciar vendas, estoque e demais recursos para a rede de restaurantes "Raízes do Nordeste"

# Testes no projeto 

Após colocar o servidor no ar, os testes poderão ser realizados por 2 meios:
* URL 127.0.0.1:8000/docs (documentação padrão da FastAPI em Swagger, com todos os PATHs)
* Collection com os testes realizados durante a implementação (que poderão ser baixada através do link: <>)

# Implementações futuras

Esta parte da fundamentação se dedica a estruturar como manter o suporte ao sistema futuramente

## Migrações no projeto

Quaisquer implementações adicionais ou alterações no banco de dados deverão seguir as seguintes etapas:
1. Alterar o arquivo de modelo, localizado na página Infrastructure/Models/Setor/Tabela
2. Após realizar a alteração, na pasta do projeto no terminal, executar:  alembic -c Infrastructure/alembic.ini revision --autogenerate -m "Mensagem"
   1. Se retornar algum erro, verificar pelo código e arquivo. As mensagens costumam indicar a origem do erro pelo próprio arquivo
3. Depois de enviado o versionamento da modelagem, executar o comando: alembic -c Infrastructure/alembic.ini upgrade head
   1. Caso retorne algum erro nesta etapa, será necessário excluir o versionamento anterior enviado. Os versionamentos ficam armazenados em: Infrastructure/alembic/versions (é possível identificar pela mensagem)