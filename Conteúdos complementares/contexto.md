# Aula 1 - Apresentação do projeto

Arquivos necessários:
* fastapi
* Uvicorn (ISGI Server) - requisições assíncronas manegadas
* SQL Alchemy - criação de BD e estrutura de modelos do abnco de dados a traduzir em tabela de forma estruturada
* Passlib[bcrypt] --> criptoografar senhas de forma segura (toda senha no BD estará criptografada)
* python-jose[cryptography] --> Permite criar tokens JWT/JSON Web Token (quando consome API, pode criar sistema de autenticação na API --> pedir pro usuário, sempre que autenticar, tem que mandar e-mail e senha, e vê se bate com o BD --> não é seguro trocar e-mail e senha a cada requisição --> criação de token [série de caracteres] com informações em formato JSON criptografado)
* python-dotenv --> manejar arquivo de variáveis de ambiente (padrão seguro)
* python-multipart (dependência do python-jose)

Comando de execução do servidor:
uvicorn main:app --reload
* reload --> toda edição feita no projeto não precisa pausar o projeto e rodar de novo

# Aula 2 - Requisições e roteamento da API

* Requisições
* Rotas diferentes
* Documentação no FastAPI

* Rotas - o que vai acontecer quando o usuário acessar um endpoint
  * EX: nomedosite.com/endpoint
  * nomedosite = domínio
  * Com o comando uvicorn, você está rodando a rota no seu domínio local (geralmente 127.0.0.1)
* No FastAPI (só com o back-end - estrutura respondendo via requisições, e consumindo via aplicação que faz requisição para a rota)
* Tipos (CRUD):
  * GET (Read)
  * POST (Create)
  * PUT/PATCH (Update)
  * DELETE (Delete)
* OBS: isso já classifica como API REST
* Informações enviadas e recebidas em formato JSON
* Criação de paths (caminhos - EX: /ordens)
* Rotas podem ser organizadas/criadas de 3 formas:
  * Tudo no arquivo main (bom se for aplicativo EXTREMAMENTE simples)
  * Criar arquivos de rotas (routes.py)
  * (caso queira segmentar rotas por módulo de uso)
    * Cuidado com importações nesse formato
    * O FastAPI vai ser usado em todos os arquivos do projeto, mas pr ele existir, não posso depender de outros elementos do projeto
      * Para não cair em importação circular (o main depende dos demais, mas os demais também dependem do main), coloca o import desse modo DEPOIS de declarar o app FastAPI
* Roteador - estrutura que cria rotas de autenticação e pedidos 
  * APIRouter --> precisa receber:
    * prefix = /path --> Em qual caminho vão existir as rotas (mais organizado, e evita conflito entre rotas)
    * tags --> nomes para organizar na documentação do FastAPI
      * Documentação no path /docs
  * Para incluir roteadores no app --> app.include_router
* Como criar rotas no roteador:
  * Usa decorator (@roteador.tipo_de_requisicao)
    * Linha de código antes de função que atribui funcionalidade nova à função ([para melhor compreensão](https://www.youtube.com/watch?v=U-G-mSd4KAE))
    * Executada sempre que tiver uma requisição desse tipo no path
  * Cria uma função logo abaixo do decorator (para associar)
    * Função async --> processos contínuos (requisições não são suspensas se uma congelar)
  * Coloca um retorno ao final da requisição (para definir o que retorna)
* Dá pra usar Docstrings ("""comentário""") para documentar a função de um path, que ele APARECE NA DOCUMENTAÇÃO!!!


# Aula 3 - Banco de Dados, Modelos e Migrações

* Criação de BD
  * Precisamos armazenar informações das rotas
  * Permite integração com várias ferramentas de construção de BD (uma das mais usadas --> SQLAlchemy)
    * ORM (Object Related Models) eficiente --> classes no Python traduzidas para tabelas no BD, e consegue usar info do BD chamando essas classes
    * Criação no BD é como criar classe no Python
    * Traduz comandos em Python para comandos em SQL no BD
    * Pode ser qualquer tipo de SQL
      * Nesse projeto, podemos usar SQLite
* Estrutura --> Arquivo models.py (para criação de classes do BD, para depois executar comando de criação de BD - BD Local para teste)
  * O deploy não terá esse BD (geralmente tem um BD no servidor que você conecta com o Models)

1. Usa create_engine do SQLite (pra conectar com um DB)
2. Criar base do BD (estrutura para construção do BD pelo Alchemy)
   1. declarative_base do orm
3. Cria as classes/tabelas do banco
   1. Toda classe recebe como pai a Base do BD (item 2) --> tradução de classe Python em tabela do banco
   2. Tabelas SQLAlchemy por padrão recebem o nome da classe em minúsculo + 's' (EX: Usuario --> usuarios), mas pode ser redefinido com __tablename__ = 'outronome'
   3. Campos definidos como parâmetros da classe
      1. importado do SQLAlchemy --> Column
      2. Cada coluna tem um tipo de dado diferente (str, bool, int, etc.)
         1. Importados também no SQLAlchemy
      3. Importa a ForeignKey também
   4. Cada coluna recebe como parâmetro:
      1. Nome da coluna
      2. Tipo de dado da coluna
         1. Se for um dado de outra tabela, usar ForeignKey --> Parâmetros:
            1. "nome_da_tabela.campo"
      3. (opcional) adição de info extra
         1.  EX: é possível criar usuário sem email? NÃO, então nullable=False
         2.  autoincrement=True (bem usado em ID, nã precisa ficar definindo em toda requisição)
         3.  primary_key=True (define a chave primária da classe)
         4.  default=False (parâmetro padrão caso não preenchido)
         5.  Se precisar que sejam valores fixos (EX: status/manter integridade de BD) --> novo import
             1.  instala no ambiente virtual --> pip install sqlalchemy_utils
             2.  from sqlalchemy_utils.types import ChoiceType
             3.  Substitui o tipo do que precisa de tipos específicos (status) para ChoiceType
             4.  Configura uma tupla de tuplas - (()) - ou lista de tuplas - [()] - para listar os tipos de preenchimentos possíveis
                 1.  Padrão chave-valor
                 2.  Chave --> o que é armazenado no BD
                 3.  Valor --> o que é visualizado se printar
                 4.  Esses itens podem ser puxados de bancos de dados também
4. Executa a criação dos metadados do banco
   1. Criação efetiva do BD
   2. Migração --> ao criar banco de dados de sistema, ao criar, já vem tudo pronto, MAS após colocar no ar, se precisar de nova funcionalidade com novo campo, precisa alterar a estrutura e todos os registros do BD
      1. Migrando o banco de dados de uma versão para outra de forma segura
      2. Biblioteca + usada para esse propósito --> alembic (dá pra fazer sem, e ao fazer migração, deletar antigo e criar novo, mas em prod não dá pra fazer)
         1. pip install alembic
         2. alembic init alembic (ferramenta do alemic para inicializar diretório alembic)
         3. alembic.ini --> configurações do processo a ser gerenciado pelo alembic (só precisa editar o sqlalchemy.url (com o mesmo link de conexão do DB de antes - único obrigatório desse))
         4. env.py --> arquivo precisa importar do models o Base (para a criação do BD)
            1. Sem alembic, colocaria ao final o comando de criação do BD
            2. Incluir import de sys e os (para puxar pastas)
            3. Colocar comando para incluir nos caminhos do arquivo para importar informações o caminho da pasta principal --> sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
               1. colocar um novo caminho na lista de caminhos que o arquivo python pode olhar
               2. Caminho da pasta onde está o projeto (idependente onde esteja)
               3. Olhando duas pastas antes do arquivo do projeto  --> '..'
               4. Depois, dá pra fazer "from models import Base", e usar no target_metadata = Base.metadata
                  1. Ao usar a base para criar os modelos, foi adicionando nos metadados as informações das classes e campos criados
   3. Ao rodar o env.py, faz um create all das tabelas
5. Para criar o BD (mesmo comando das migrações) --> alembic revision --autogenerate -m "Migracao inicial"
   1. --autogenerate --> auto gera o arquivo de migração (na pasta do alembic/versions), que dita como vai ocorrer a migração no Python para o BD
      1. Migrar estado inicial do BD pro final
6. Para executar migração oficial --> alembic upgrade head
   1. MAS sqlalchemy.utils e alembic não integram tão bem, e por isso, precisa editar manualmente arquivo de versionamento (colocando)
   2. Solução --> mudar de ChoiceType como String mesmo, e restringe pelo processo de criação do bd, e Schemas
      1. Simplifica a migração do BD, e dá mais flexibilidade (só precisa editar no Schema depois)

# Aula 4 - Criar conta de usuário, schemas e criptografia

* Estruturar processo de criação de itens no BD
* Garantia de sessões de dados robusta e escalável
  * Sem problema de conexões abertas/fechadas
* Schemas (usada para padronizar envio de dados no sistema, respostas do sistema, etc)

* Criação de pedidos de usuários autenticados
  * Rotas de autenticação
* Nessa aula, será criada uma forma de autenticação não muito segura, mas simples (na próxima aula, aprofundaremos mais)
  * Mais pela troca de informação
* Toda informação enviada em um post da rota será recebida pela função
  * EX: email e senha
  * Recomendação: **sempre** defina o tipo de dado
    * Mantém a integridade
* Precisa validar também se o usuário já existe no DB
  * Pegar sessão do DB para verificar
    * Qualquer edição no DB depende de uma sessão --> conecta, edita e salva/commita
  * Em sistemas online, é comum ter limite de conexões a fazer no BD ao mesmo tempo
    * Gerenciar de forma eficiente
      * from sqlalchemy.orm import sessionmaker
      * Cria uma classe sessão com sessionmaker
        * Propriedades: bind=bd (lá dos models)
      * Cria uma instância da classe de sessão. Eis sua sessão
      * Dessa sessão, faz um query para o modelo Usuario, e filtra
        * usuario = sessao.query(Usuario).filter(Usuario.email==email).all() - confere se tem algum, e retorna um número
        * usuario = sessao.query(Usuario).filter(Usuario.email==email).first - confere se tem algum, e retorna um Usuario
      * Se tiver usuário, retorna mensagem de erro
      * Senão, cria
        * Cria uma nova instância de usuário, e dá um sessao.add(variavel_com_usuario)
        * Dá um commit na sessão
          * Pega as alterações e comitta o banco de dados (pra não ficar editando o tempo todo)
    * Precisa finalizar depois de criar
* Problemas de segurança
  * Sessão está sendo aberta, mas não necessariamente está fechando (se der um erro no meio, ele não fecha)
  * Erro de cadastro deve retornar código diferente de 200
  * Ao invés de mandar os dados isolados, posso pedir para só mandar uma instância de usuário para criação
* Para testar, dá pra colocar os campos pelo docs
* Melhorando o gerenciamento de sessão:
  * Toda rota precisa editar algo no BD, mas a repetição de criação de sessão sobrecarrega
  * Sessões iniciadas, mas não necessariamente finalizadas
    * Comando: sessao.close()
    * Ainda,  se quebra, ele não chega no final
      * Prática ideal - a sessão é algo que todas as rotas DEPENDEM --> dependancy
      * Cria dependência (função) para criar sessão, e dar à rota
        * Dependência - função que devolve um elemento/parâmetro, que vem de função em outro lugar
        * Cria arquivo de dependências
        * Cria método de gerar sessão
        * Adicionamos parâmetros da função de post
          * Ainda pode ser alterada pelo usuário
          * Para especificar que vêm de dependência --> from fastapi import Depends
          * sessao = Depends(pegar_sessao) --> especifica que essa função gera uma dependência
      * Quando a rota finalizar (independente como), fecha o db
* Agora, consigo criar sessão para todas as rotas (basta seguir esse mesmo modelo)
  * Mas sessão ainda não está sendo fechada
  * Como fechar a sessão após retornar a sessão?
    * Ao criar instância da classe Session, por padrão, ele vira um generator do Python --> lista de itens, mas não com a lista toda carregada(só o generator)
    * pegar 1º elemento da lista --> yield
    * Ao invés do return, dá um yield
      * Não encerra mais a função, e ele só retorna um valor sem encerrar execução da função
  * Agora, ele fecha, mas só se termina a execução
    * Se der erro, trava no yield
      * Só colocar os blocos em try-except
* Como customizar o código de erro?
* Como passar as informações em parâmetros?
* Como armazenar senhas criptografadas?
  * String de senhas criptografadas
  * Usaremos o bcrypt
    * Importa no main
    * from passlib.context import CryptContext
    * Para funcionar, você precisa criar chave (que garante segurança da criptografia)
      * Pega o texto do usuário, pega uma chave secreta no sistema, e combina as duas (a partir de um algoritmo) para criar a chave criptografada
      * Para desvendar a senha, precisa da chave secreta (armazenada no .env)
        * Pode buscar uma secret key de um site gerador mesmo, ou pegar o módulo secret do Python (pode pegar uma forte)
        * NÃO PODE APARECER EM NENHUM OUTRO LUGAR (não sobe pro git)
      * Agora, precisamos importar a info da variável de ambiente pro programa
        * python-dotenv
        * from dotenv import load_dotenv
        * Roda a função
          * Carrega variáveis do .env do mesmo ambiente
          * SECRET_KEY = os.getenv("SECRET_KEY")
      * Depois de criar o aplicativo, carrega o CryptContext
        * Quando for armazenar senha, ou confirmar a senha, pede pro bcrypt_context (verificando se é a mesma senha do BD)
          * Não descriptografa a senha, só verifica se é a mesma armazenada no BD
        * bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
          * deprecated --> pode passar mais de um esquema de criptografia, e se algum ficar obsoleto, ele só descarta e para de usar
    * Como usar na rota de autenticação?
      * Na hora que o usuário passar uma senha, não salva ela direto no user
      * Importa o bcrypt_context do main
      * senha_crypt = bcrypt_context.hash(senha)
        * OBS: versão 5.0.0 do bcrypt conflitando com passlib (mudar p/ versão 4.3.0) --> muda no requirements --> pip install -r requirements.txt
  * Verificação da senha na etapa de login
* Como responder usuário com mensagens de erro customizadas
  * Retorno em dicionário costuma retornar código 200 (de sucesso)
  * Qualquer código 400 e alguma coisa indica erro
  * Usaremos 400 para erradas e 200 para certas
    * Do fastapi, vamos importar HTTPException
    * Retorno de erros --> raise HTTPException(status_code=400, detail='E-mail do usuário já cadastrado')
      * Levanta o erro
* Como enviar info pra função (Schemas)/Personalizar entrada para funcionar
  * Em programas mais robustos, costuma se criar um arquivo schemas.py
  * Schemas - estruturas do python, na qual usamos o Pydantic
    * Estrutura para forçar tipagem de dados (porque o Python não obriga) --> Pydantic obriga, e isso garante integridade de dados, e o sistema fica mais rápido (corta validação de tipo de dado)
    * Objetivo --> velocidade e integridade (recomendado pra FastAPI)
  * Não envia dados fixos, envia uma classe
    * from pydantic import BaseModel --> Todas as cllasses são subclasses do modelo base do Pydantic
    * Tipos de dados importados do typing - dados opcionais, por exemplo
      * from typing import Optional
      * ativo:Optional[bool]
  * Como conectar com o modelo?
    * Cria uma classe dentro dessa classe --> class Config: \n from_attributes=True --> A classe não deve ser interptetada como um dicionário, mas como um ORM (Object Related Model) --> Classe transformada em SQL
    * Ao invés do nome e senha, passa um usuario_schema:UsuarioSchema
    * Por padrão, é bom especificar o tipo de tudo passado como parâmetro (mesmo a session, que já recebe um valor padrão, por segurança mesmo)
    * Passando schema dessa forma, estrutura melhor para ter todos os campos sendo enviados para a criação do novo usuário
  * Traz visualização do Schema no docs também (campo Schemas, abaixo das requisições) e traz até um modelo para preenchimento da requisição, com base no schema
    * Requisição feita por código precisa enviar código json (seguindo o Schema de visualização)
    * No Try it Out, agora ele permite preencher json
    * Obrigação de seguir esse schema de envio (envio padronizado por um único objeto)
  * Por que é melhor?
    * Não recebe vários parâmetros, apenas 1 (usuário) com os parâmetros do schema --> mais organizado
    * Já vem com o exemplo de preenchimento do schema, no qual saberemos o que enviar
    * Padronização de entrada de dados
* Estrutura + verbosa que o Flask/Django
  * Para funcionar mais veloz, usa async, schemas, tipagem de dados (para não gastar tempo do sistema/memória fazendo esses processos)
  * Mais tempo para construir, MAS no ar, é mais fácil de executar
  * Resultado final --> API mais rápida, graças às estruturas

# Aula 5 - Criar Pedidos e Fazer Login

* Construção de endpoint de login "menos seguro"
* Nas próximas aulas, veremos autenticação e tokens

* Por que rota de login?
  * Apenas usuários logados poderão criar/editar pedidos
  * Processo de login depende de token (no qual você envia login e senha apenas uma vez, ele devolve um token, e você usa ele para acessar rotas)
  * Token será usado nas rotas de pedidos (não manda email e senha, só o JWT - JSON Web Token)
    * Armazena várias informações em série de caracteres
    * Mais seguro que sempre enviar e-mail e senha (exposição em vários endpoints)
    * Tokens podem expirar
      * Pode fazer requisição por tempo limitado
      * Maior segurança no sistema
* Primeiro rota de criar_pedido
  * Mesmo padrão do de autenticação na criação da de autenticação praticamente
  * Pedidos sempre terão status específicos (mas o usuário não precisa enviar)
  * Tudo que o usuário precisa enviar de fato é o id do usuário
* Estrutura de login (para só usuários logados poderem criar pedido)
  * Login --> email/senha --> Token JWT (JSON Web Token) nsdcbvasjdfbi (decodificado, podemos identificar as informações do usuário - ID, email,  etc.)
    * Token - identificação do usuário (Tem tempo de expiração)
  * Como validar que o usuário é ele mesmo?
    * Em cada rota de usuário logado, precisa receber OBRIGATORIAMENTE como parâmetro o token
  * Precisa de schema específico para login
  * Login = passagem de token para o usuário
    * Função separada criar_token()
    * Token = Token Bearer (quando faz requisição pro endpoint, tem que mandar nos headers da requisição um parâmetro "Access-token": "Bearer Token")

# Aula 6 - Autenticação, OAuth2 e JWT Tokens

* Autenticação de usuário
  * Para evitar descriptografia (falha de exposição de senha), dá pra comparar os hashes para ver se são iguais (o hash gerado pelo schema seria igual ao hash salvo no DB?)
  * Criar função separada para autenticar_usuario
    * Nessa função, terá a mesma validação de existência de usuário ou não
    * Além disso, terá a validação da senha
      * bcrypt.verify (recebe a senha, a hash (da tabela de usuário), e compara)
  * JWT - JSON Web Token --> [JWT](http://jwt.io)
    * Token grande nesse formato de caracteres
    * Ao decodificar, pode-se descobrir info
    * Token que armazena JSON de informações (EX: identificação de usuário, e data de expiração)
    * Vamos gerar nosso próprio JWT
      * Vamos armazenar ID do usuário e data de expiração
      * Nova geração de token pode ser por email e senha, OU por meio de um refresh-token (com duração maior, mas para permitir gerar um novo - não precisa enviar constantemente) - depende das regras de segurança
      * Para criar, precisamos importar algumas informações na main (criar 2 variáveis de ambiente)
        * ALGORITHM - algoritmo de criptografia do token (um dos mais populares é o HS256 - impossível de ser descriptografado, só por força bruta, a não ser que tenha a chave que fez isso)
        * ACCESS_TOKEN_EXPIRE_MINUTES - todo token terá x minutos de duração (padrão) - tem que converter em int na main
      * Depois, podemos utilizar algumas libs para gerar esse token (+ atual do FastAPI - python-jose)
        * from jose import jwt, JWTError
      * Também preciso de bilbioteca de tempo do dia
        * from datetime import datetime, timedelta, timezone (fuso-horário)
        * data_expiracao = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
          * Definindo que o horário de expiração será a hora atual (segundo o fuso UTC) + tempo de expiração (importado da main)
        * Criar também dict_info (informações que serão usadas no header para identificar o usuário - id e data de expiração)
          * Pela documentação do JWT, "sub" geralmente representa o id em JWT
        * Para codificar - variavel_a_guardar = jwt.encode(dicionario_de_info, chave_secreta, algorithm)
          * chave_secreta - referência da condificação (exclusiva do sistema)
    * Com isso, se jogar no jwt.io, ele ainda vai identificar como um JWT válido, mas não sabe reconhecer (por não ter nossa SECRET)
      * Mas se passa, ele consegue descriptografar
      * As pessoas até podem conseguir as informações do Token, MAS não vão conseguir se passar por você (já que o token não é o mesmo que geraria com uma chave de segurança qualquer)
  * Refresh token costuma ter duração maior que o access (nas requisições, sempre manda o access token) - ao invés de passar email e senha, passa o refresh, e gera um novo access token
    * No login, cria ambos - direrença será a duração
      * Novo parâmetro para criar_token = duracao (padrão será o timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        * Dessa forma, ao passar o novo, não precisa ficar contando na cabeça quantos minutos teria em 7 dias, por exemplo timedelta(days=7)
    * Passa o refresh junto no retorno
      * O usuário até poderia usar o refresh no lugar do access para autenticar, mas perderia a proposta da segurança
      * Lógica - Quando vence o access token, dá um refresh token e se gera um novo access token para requisição
  * Falta gerar novo access_token com base no refresh_token - nova rota
    * Precisamos definir qual parâmetro passar ao usuário (token do usuário - refresh)
    * Precisa ser um token com signature válido
      * Pega as info do token descriptografado e valida se pertence ao usuário mesmo
      * A função de verificar token precisa virar dependência
        * Em toda rota que receber token como parâmetro, o token precisa ser uma dependência da rota - pro usuário acessar a rota, envia um token válido
        * Sempre que usar o Depends para criar uma dependência, precisa ser usada como parâmetro da função a ser usada na rota (não pode usar diretamente em função dentro da rota)
        * verificar_token vai virar Depends

# Aula 7 - Bloqueio de Endpoints para Usuários Autenticados

* Permitir que apenas usuários autenticados possam acessar partes da sua API
  * Cadeados no docs da API
* Verificar token precisa virar dependência antes
  * Para rodar função com parâmetro depends, teria que vir como parâmetro da rota - dentro da definição da rota (def da função da rota)
  * Por que o token também tem que ser dependência do BD?
    * Quando for criar rota de pedido, precisamos que o usuário esteja autenticado
    * TODAS as requisições da rota de pedidos demandam autenticação
    * Ao invés de colocar sempre a função de verificar_token no código principal, coloca como dependência (a ser usada nas funções)
      * Se quiser login para rota específica, coloca o verificar_token
      * Garante acesso à rotas apenas se estiver logado na rota
    * O verificar_token retorna um usuário, então o refresh_token precisa receber um usuário como parâmetro
      * Precisa enviar um token para a requisição
      * Quando enviar, pega o token e dá como resposta o usuário, e cria o access_token
  * O token sendo enviado ainda não está sendo lido
    * Vamos decodificar o token enviado
    * jwt.decode (mesma coisa do encode)
      * Se alguma parte do processo de decodificação der errado, precisa levantar JWTError
      * 2 formas de pegar item de dicionário
        * dicio.get('campo') e dicio['campo']
        * Diferença é que o get não dá erro se não achar, só não retorna nada
  * O token ainda precisa ser enviado em um formato específico
    * Token Bearer normalmente não precisa ser enviado como parâmetro da requisição
    * Tipo de autenticação por token bearer - OAuth2
      * Esse padrão indica que o token precisa ser enviado como header, com nome Access-Token: Bearer cvsdbgksebvku
    * O token deve ser enviado nos headers (fora do body)
      * Até dá pra adaptar pra enviar pelo body, mas é melhor seguir o padrão
  * O Token do verificar_token, assim como a session, deve ter uma classe especifica associada (schema - OAuth2Schema)
  * Depois da definição do bcrypt no main, configura um oauth_schema
    * from fastapi.security import OAuth2PasswordBearer
    * oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/login')
    * def verificar_token(token:str=Depends(oauth2_schema),sessao:Session=Depends(pegar_sessao)):
      * token tratado como dependência do Auth
  * Token enviado como parâmetro deve vir como header da requisição do refresh
  * Usar oauth viabiliza uso de token em header
    * Novo botão de authorize no docs
    * Permite login para usar token bearer no header
      * Login retorna o access token, a ser usado em tudo
      * Ainda precisa criar o formulário de autenticação
* COMO TESTAR?
  * Arquivo de testes
  * Bibloteca requests
    * requests.get("link/auth/refresh", headers={dict_de_headers})
  * Toda requisição feita ao sistema que use o Depends dentro da função OBRIGATORIAMENTE deve enviar token dentro do header da requisição (chamado authorization, com estrutura do bearer)
* Estrutura de autenticação do refresh token pronta
* Dependência de verificar token pronta
* Com oauth_scheme pronto!
* Só falta o botão de autorização (para testar endpoints protegidos direto na documentação)
  * Pela validação, dica de ouro: erros JWT podem ser diagnosticados com print no try-except
  * Problema na verificação do token
    * sub de identificação do usuário ainda deve ser armazenado como str (converte lá na criação do token em str)
* Toda requisição que quisermos fazer, em qualquer endpoint que exija login, no header pode mandar token de autorização que passa pela verificação e retorna quem está requisitando
* Criação de botão do login no docs
  * "2º endpoint de login"
  * Botão de Authorize
    * Atualmente, recebe login_schema (com email e senha)
    * Poderia, em um frontend, colocar lógica de extrair info do formulário e enviar como requisição para fazer login
    * Copia a rota de login e cria uma nova a partir dela
      * Ao invés de passar login_schema, passaria um formulário OAuth2 - para tratar autenticação de bearer
      * Passa dados de formulário como parâmetro (vindo do FastAPI.security)
        * from fastapi.security import OAuth2PasswordRequestForm
        * Instância de classe do objeto dados_formulario
        * Dependência que vêm vazia - preenchida automaticamente ao clicar em Authorize no Docs
        * Não precisa da função por ser um formulário que já está na tela (por padrão, o formulário já te dá os dados do formulário, não precisa criar função pra extrair)
  * Correspondências para funcionar de acordo:
    * username = email
    * email=dados_formulario.username
    * Esse novo processo de autenticação não precisa de refresh_token (só do access, que será usado na prática)
    * Muda também a rota padrão para autenticação do Authorize por uma rota diferente da padrão
      * Não altera o login padrão, só dá uma nova possibilidade de login por meio do botão
      * ATENÇÃO PARA DIGITAÇÃO, PELO AMOR DE DEUS!!!!! (access_token usa underline, não traço)
      * O access_token usado para o header do refresh é o mesmo que foi gerado no Authorize (e salvo nas requisições, a ser usado em qualquer endpoint)
* Resumão da autenticação
  * Sempre cria um usuário (a definir depois quem poderá criar usuário)
  * Obriga envio de token
    * Dá pra saber quem é o usuário pelo token
    * É possível bloquear rotas agora
  * Endpoint de criar usuário
    * Mesmo que não seja obrigatório a todos
  * Endpoint de login (e login por formulário)
  * Endpoint de refresh token
  * Faz login com email e senha, e usa o access_token para acessar as rotas (coloca a dependência de verificar_token - que só valida se fizer login)
  * Vamos bloquear endpoints (para apenas usuários autenticados criar pedidos, ver status de pedido, etc)
  * Vamos mexer também com níveis de acesso

# Aula 8 - Níveis de acesso e Lazyloaded do Banco de Dados

* Reconstrir rotas para bloquear acesso de acordo com nível de acesso
* Criar regras personalizadas (para bloquear níveis de acesso)
* Ideias a implementar
  * Cancelar pedido
  * Adicionar item em pedido
  * Editar pedido criado
  * Finalizar pedido
* Cancelar pedido
  * Para garantir que apenas usuários autenticados possam cancelar, passa o schema de usuário como parâmetro da função
  * Quero que seja aplicado em todas as rotas
    * Pode passar como parâmetro NO ORDER_ROUTER
      * Parâmetro dependencies --> lista de dependências a serem aplicadas em todas as rotas do roteador
      * Quando usa dependência na rota, dá pra usar a resposta como parâmetro na função
  * Nas rotas que quiser ter o usuário separado, daí passa normal
  * Cancelamentos são método POST
    * Se quiser que o id de cancelamento faça parte também da rota --> Passa como parâmetro entre chaves
    * Obrigatoriamente precisa passar a mesma coisa como parâmetro
      * Na URL --> Parâmetro de URL
      * Na função --> parâmetro de body
  * Cancelamento de pedido requer edição no BD --> liga uma session
    * Não esquece do commit
      * Só precisa dele, porque você não está adicionando nada novo
  * Após encerrar a sessão do BD (commit), ele encerra a conexão com o BD e zera os campos vinculados ao BD
    * FastApi usa LazyLoaded - carrega apenas as informações que precisa carregar do BD
      * Se puxa pedido, puxa a instância do pedido, mas não puxa todas as informações do pedido
  * Nível de acesso - quem pode cancelar o pedido?
    * No momento, qualquer pessoa, mas não faz sentido
    * Faria sentido se fosse o próprio usuário do pedido, ou usuário admin
    * Se precisa validar nível de acesso, precisa receber usuário como parâmetro
      * Não tem problema ter dependência na rota e no path
      * elif not usuario.admin and usuario.id != pedido.usuario:
    * Interrupção da execução da rota quando identificar que o usuário não está fazendo o que é esperado
* "Resolver" problema do Lazyloaded (carregamento preguiçoso)
  * Não é um problema, é um sistema eficiente
  * Quando pega pedido, ele não traz tudo logo de cara (carrega instância do que é pedido) - só carrega quando solicitado
  * No models, temos info dos pedidos (ao carregar o pedido, não precisa identificar todos os campos de uma vez) - processo + rápido e leve
  * Para salvar, precisa carregar info do pedido que obriga o BD a carregar os detalhes do pedido
    * Ao invés de no cancelar_pedido colocar no return o id_pedido recebido como parâmetro, passa o pedido.id (isso força o BD a carregar info do pedido, e carrega as demais infos do pedido)
      * Carrega todos os campos do elemento por padrão, em dicionário de informações

# Aula 9 - Adicionar item em Pedido e Relationship em Models

* Endpoint para listar pedido
* Endpoint para adicionar item no pedido
* Entender Lazyloaded no retorno das informações
* Como conectar diferentes tabelas do BD nas duas direções - add item e no pedido puxar todos os itens que fazem parte do pedido

* Endpoint de listar pedido
  * Basta colocar validação do usuário e sessão e sucesso!
* Adicionar item no pedido
  * Cria uma nova função com parâmetro de path do id_pedido
  * Importa model do item-pedido (para usar de referência na criação)
    * Schema não precisa do número do pedido (já que isso já vem como query param)
    * Lembrete para não esquecer: o Schema é um modelo para garantir integridade, mas o que vale de fato são os Models
      * No exemplo acima, poderia simplesmente adicionar o id_pedido no final do Model, sem exigir no Schema
  * Como atualizar o preço do pedido ao adicionar itens dinamicamente?
    * Já está vinculado ao pedido graças à Foreign Key
    * Dica: sempre que atualizar/adicionar produtos, atualiza o preço do pedido
    * Dá pra fazer dentro da classe pedido
      * Cria método calcular_preco - percorre lista de itens (salva no model em si), depois soma todos os itens e edita o campo "preco"
      * 2 opções para busca - ou adiciona uma session para fazer a busca pelos itens com id do pedido igual ao seu pedido OU cria campo de itens dentro da classe direto - conexão automática
        * Sempre que conectar 2 tabelas, e precisar na tabela original puxar as informações de outra tabela, cria relationship (campo importado do SQLAlchemy)
        * Relação do campo x com campo y (não é necessariamente dependência, pois ela já existe, só é o caminho contrário da chave estrangeira)
        * relationship("NomeDaClasseVinculada)
        * Parâmetro cascade="all, delete" --> Quando deletar um pedido específico, vai cascadear esse processo para todos os itens relacionados ao pedido
        * self.itens já vira automaticamente TODOS os itens do pedido
  * Como criamos um novo campo, precisamos fazer o migration
    * Campos de relationship não aparecem diretamente como coluna
  * Atenção sempre para a ordem de execução
    * Se tentar executar cálculo antes do item ser adicionado, vai ficar inconsistente

# Aula 10 - Finalização e Schemas para Respostas de Endpoints

* Finalizar projeto
* Regular níveis de acesso (para editar e puxar informações dos pedidos)
* Padronização de resposta do banco de dados (usando schemas do fastapi) - Fácil escalabilidade das construções de API eficiente

* Remover item de pedido
  * Não precisa do id_pedido, só do item do pedido (já tem tudo a partir dele)
  * Só permite excluir se for dono do pedido do qual o item faz parte
    * Campo pedido é um id de pedido, então tem que fazer outra busca pelo pedido
    * Cada item tem um id individual (que o usuário não precisa ficar vendo)
    * O LazyLoaded também se aplica para campos dentro de campos (campo itens só carrega se chamar exclusivamente)
* Definição das últimas rotas da API
  * Visualizar 1 pedido
  * Finalizar um pedido
    * Bem similar ao de cancelar
  * Visualizar todos os pedidos de 1 usuário
    * Basta filtrar pelo usuário (que pode ser passado como parâmetro ou lido do próprio usuario logado)
* Criar padrão de schema de resposta
  * Não precisamos de todas as informações sempre
  * Para padronizar saída, precisa de schema - do mesmo jeito dos anteriores
    * Para aplicar --> chama o schema nos parâmetros DA CRIAÇÃO DO ENDPOINT
    * Exibe o retorno no padrão do response_model
  * No caso de schemas de lista, ou dá pra criar um schema específico de lista, ou importar do typing(pydantic) o List
    * List[Schema]
    * Como já está em lista, não precisa retornar em dict específico
    * Se quer colocar List nos schemas direto também (itens detalhados) --> List[NomeDoSchemaDosItens]

* Finalização
  * Principais métodos relevantes
  * Back-end completo de RESTAPI
  * Mesmo processo de back-end de site (conectado a front-end que consome as rotas)
  * AI pode ser publicada desta forma
  * É legal colocar orientações nas rotas, e uma homepage explicando tudo
  * Tenta fazer um deploy, ou conectar com um front