# Roteiro geral

O que envolve cada etapa:
* Compreensão do problema
	* [[Regras de Negócio]]
* Tomada de decisão técnica
	* [[Escolha da ferramenta]]
	* Resolução de ambiguidades
* Coerência da solução proposta
	* Funcionaria em um contexto real?
	* Faz sentido com o que foi estabelecido pela empresa? --> [[Regras de Negócio]] 

Requisitos gerais
* Deve ter link do repositório no GIT
* Estrutura do documento principal:
	* Capa e Sumário
		* Curso, disciplina, nome, RU, Polo de apoio, semestre e professor
		* Sumário com organização do documento
	* Introdução
		* Contexto do estudo de caso
		* Objetivos do projeto
		* Principais usuário
		* Relevância do sistema
	* Análise de requisitos
		* Requisitos funcionais e não funcionais (em tabelas ou listagens caso queira)
	* Modelagem e Arquitetura
		* Diagrama de caso de uso
		* Diagrama de classes
		* DER (Diagrama Entidade-Relacionamento)
		* Descrição dos endpoints da API
		* Tecnologias de persistência
		* etc.
	* Entrega Técnica
		* Segue o roteiro de trilha
		* Deve incluir artefatos e evidências exigidos
	* Plano de Testes e Evidências
		* Estratégia de validação
		* Apresente os cenários de teste com critérios de aceitação
			* Entradas
			* Passos
			* Saídas esperadas
		* Inclua cenários positivos e negativos (erros)
		* Apresente conforme o requisitado no roteiro da trilha
			* Coleção Postman
			* prints do protótipo
			* Relatório de testes automatizados
			* Registros de execução
	* Conclusão
		* Principais lições aprendidas
		* Desafios
		* Pontos de atenção para evoluções futuras
	* Referências
		* Livros, sites, artigos, etc que subsidiaram o trabalho
* Materiais suplementares
	* Modelos UML 
		* diagramas de atividade
		* diagrama de sequência
		* diagramas de estados
		* diagramas de componentes
		* diagrama de implantação
		* se julgarem necessário
	* Código fonte importante (para apoiar indicações no texto ) - indique a referência
	* Prints de tela de protótipos e testes
	* Scripts de teste / resultados de automações

## Critérios de avaliação

1.  Estrutura, Organização e Clareza do Trabalho (10%)
	* Como o trabalho é organizado e apresentado
	* Critérios:
		* Apresenta claramente o contexto da rede Raízes do Nordeste, e o problema a ser resolvido
		* Organiza o conteúdo de maneira lógica, com textos coerentes e objetivos.
		* Identifica corretamente a trilha escolhida (Back-end, Front-end ou Qualidade de Software).
		* Utiliza diagramação, tabelas, fluxos, diagramas ou protótipos que facilitem o entendimento do trabalho.
2. Qualidade da Documentação e Análise do Negócio (30%)
	* Entendimento do negócio e regras do sistema
	* Critérios:
		* Levantou e descreveu corretamente os requisitos funcionais e não funcionais do sistema
		* Considerou aspectos como:
			* Múltiplos canais de atendimento
			* Diferença entre unidades da rede
			* Controle de estoque e relatórios para a matriz
			* Programa de fidelização e conformidade com a LGPD
			* Integração com serviços externos de pagamento
		* Justificou as decisões técnicas com base no cenário
		* Demonstrou atenção às ambiguidades e desafios reais do problema
3. Modelagem, Arquitetura da Solução ou Protótipo (30%)
	* Qualidade da solução técnica proposta
	* Critérios:
		* Apresenta solução coerente com os requisitos definidos
		* Desenvolveu diagramas, arquiteturas ou protótipos consistentes e claros
		* Considerou aspectos como:
			* escalabilidade
			* integração entre sistemas
			* tolerância a falhas
			* crescimento da rede
		* Informou o link do repositório do código corretamente, e/ou da ferramenta de prototipagem utilizada
	* OBS: se o link estiver indisponível, este item receberá nota zero
4. Plano de Testes e Estratégia de Qualidade (20%)
	* Preocupação com qualidade, segurança e confiabilidade do sistema
	* Critérios:
		* Definou estratégia de testes adequada ao cenário da rede
		* Incluiu testes:
			* fucionais
			* não funcionais (desempenho, disponibilidade, usabilidade, etc.)
			* de segurança e privacidade (LGPD)
			* de integração com serviços externos
		* Descrever claramente cenários de teste e critérios de aceite
		* Demonstrou atenção aos riscos do sistema em horários de pico
5. Aplicação Prática, Originalidade e Postura Profissional (10%)
	* Maturidade da proposta como solução real de mercado
	* Critérios
		* Propôs solução aderente ao contexto apresentado
		* Apresentou decisões técnicas bem fundamentadas
		* Utilizou boas práticas e referências do mercado
		* Demonstrou postura profissional, pensando no trabalho como algo que poderia ser apresentado em:
			* Uma empresa
			* Um estágio
			* Uma entrevista técnica

## Dicas

* Cronograma: divida a atividade em etapas (requisitos, modelagem, implementação, testes) para não deixar tudo para o último momento. 
* Ferramentas Úteis: 
	* Modelagem: Lucidchart, Draw.io, Astah, Visual Paradigm. 
	* Protótipo de Telas: Figma, Adobe XD, Canvas, Marvel App. 
	* Testes: Selenium, Cypress, JMeter, OWASP ZAP.
	* Documentação: Google Docs, Microsoft Word, Latex.
* Revisão Final: antes de postar, revise o PDF para garantir que todos os itens solicitados estejam presentes.


# Roteiro Back-end

* Objetivo --> Avaliar capacidade de:
	* analisar estudo de caso
	* modelar dados
	* Definir contratos de API
	* Implementar solução de back-end que atenda aos requisitos funcionais e não funcionais do cenário
* Demonstrar domínio de:
	* Levantamento e priorização de requisitos (o que é essencial e por que)
	* Modelagem do domínio e da base de dados (DER e entidades, relacionamentos e integridade)
	* Arquitetura e organização do projeto (camadas, separação de responsabilidades, padrões de projeto)
	* Implementação de API REST com endpoints coerentes, contratos bem definidos e documentação (Swagger/OpenAPI)
	* Persistência em banco de dados com consistência entre modelo e implementação (migrations/ORM, seed quando necessário)
	* Regras de negócio do fluxo crítico (pedidos, estoque por unidade, atualização de status, fidelização)
	* Integração simulada de pagamento (mock) para demonstrar fluxo completo (sem depender de provedores reais)
	* Segurança e LGPD (mínimo técnico)
		* Autenticação
		* Autorização por perfis/roles
		* Cuidado com dados pessoais
		* Armazenamento seguro (ex: hash de senha)
		* Respostas sem exposição indevida de dados
	* Qualidade e testabilidade -- plano de testes com cenários positivos e negativos, e evidência reproduzível (coleção Postman/Insomnia e/ou testes automatizados)
* Apresentar solução que execute, seja reproduzível (com README explicando a execução) e comprove domínio dos elementos essenciais de um back-end profissional (conforme requisitos e limitações definidos)

## Introdução e objetivos

Esta atividade simula um cenário real de mercado onde o aluno deve projetar uma solução robusta para uma rede de lanchonetes em expansão. O foco está na **compreensão do negócio**, na **tomada de decisão técnica** e na **entrega de uma API/solução de Back-end que suporte múltiplos canais (App, Totem e Web).** 

## Análises e requisitos

* Listar requisitos com foco em regras de negócio, persistência, integrações e segurança (sem telas)
	* Requisitos funcionais: cadastro e autenticação (login), gestão de unidades da rede, cardápio por unidade, gestão de pedidos (criar, atualizar status, cancelar), controle de estoque, programa de fidelização e integração com serviço externo de pagamento (mock)
		* Deve contemplar todos os requisitos necessários ao funcionamento completo do sistema, incluindo os requisitos obrigatórios a seguir:
			* Cadastro e autenticação dos usuários (incluindo perfis/roles)
			* Visualização/consulta de cardápio por unidade (API)
			* Realização de pedidos (com itens, valores, status)
			* Atualização do status do pedido (cozinha --> pronto --> entregue/cancelado)
			* Controle de estoque (entrada/saída e restrição de venda por indisponibilidade)
			* Programa de fidelização (pontos e resgate simples, com consentimento)
			* Promoções/campanhas (ao menos com documentação de como aplicar)
			* Solicitação de pagamento via serviço externo (mock) + registro
				* NÃO DEVE SER PAGAMENTO REAL, mas demonstrar fluxo de envio do pagamento e retorno da API (status e payload) para o cliente (App/Totem/Web)
		* Multicanalidade (domínio) (OBRIGATÓRIO)
			* Deve atender múltiplos canais (App, Totem, Balcão, Pickup, Web)
			* Deve tratar canal de origem do pedido como dado de domínio, registrando esse dado no pedido e garantindo rastreabilidade entre canais
			* MÍNIMO:
				* Pedidos devem ter campo canalPedido (ENUM) com valores:
					* APP
					* TOTEM
					* BALCAO
					* PICKUP
					* WEB
				* Criação de pedido deve exigir o preenchimento de canalPedido
				* A API deve permitir consultar/filtrar pedidos por canal
					* EX: query param ?canalPedido=TOTEM
			* Objetivo: permitir consolidação e acopanhamento do fluxo de pedidos por canal
				* Integração e consistência do atendimento na rede
	* Requisitos Não Funcionais: segurança (LGPD, controle de acesso, senha com hash, token), logs/auditoria de ações sensíveis, desempenho em horários de pico, disponibilidade do sistema, tolerância a falhas de integração de pagamento e documentação (OpenAPI/Swagger)

## Diagramas

Fundamentam a lógica da solução e são requisito para a avaliação de visão sistêmica

1. Diagrama de Casos de Uso
	* Elaboração com os atores:
		* Cliente (App/Web/Totem)
		* Atendente (Balcão)
		* Cozinha
		* Gerente/Administrador
		* Sistemas Externos de Pagamento (Gateway)
	* Descrição da Feature (obrigatória)
		* Escolha funcionalidades críticas
			* Realizar Pedido + Solicitar Pagamento
		* Detalhe o fluxo principal, pré-condições, pós-condições, exceções e regras de negócio
			* [Idempotência](https://www.youtube.com/watch?v=YNHKO_74sLU) 
			* Estoque insuficiente
			* Pagamento negado
2. DER (Diagrama Entidade-Relacionamento)/Modelo de Dados
	* Apresentar DER de banco de dados com entidades, atributos principais e relacionamentos
	* Inclua chaves (PK/FK), cardinalidades e restrições relevantes
		* EX: Unidade com estoque próprio; Pedido possui itens; Pagamento é desacoplado
3. Arquitetura (camadas e separação de responsabilidade) - OBRIGATÓRIO
	* Deve apresentar estrutura por camadas (ou equivalente), explicitando separação de responsabilidades entre:
		* Domain (Domínio): entidades, regras de negócio, validações e comportamentos do domínio (EX: Pedido, Cliente, Produto, Estoque)
		* Application (Aplicação): casos de uso/serviços que orquestram o fluxo do sistema (EX: criar pedido, aplicar fidelidade, confirmar pagamento mock, atualizar status)
		* Infrastructure (Infraestrutura): persistência (ORM/migrations/repositórios), integrações (pagamento mock, e-mail/log), e detalhes técnicos
		* API (Interface/Controllers): rotas/endpoints, autenticação/autorização, contratos de request/response e documentação (Swagger/OpenAPI)
	* OBS: pode adotar variações (como MVC, Clean Arquitecture ou DDD simplificado), desde que a separação de responsabilidades foque clara no código e na documentação (foco da avaliação na coerência e clareza de organização)
4. Diagrama de Classes (obrigatório) e Sequência/Atividade (recomendado)
	* Diagrama de classes (visão de domínio) com as principais entidades/objetos e relacionamentos
	* Diagrama de sequência ou atividade do fluxo crítico (Pedido --> Pagamento Externo --> Atualização de Status)

## API E ENDPOINTS (OBRIGATÓRIO)

* Descrever principais endpoints da API, organizados por recurso
	* EX: /auth, /unidades, /produtos, /estoque, /pedidos, /fidelidade, /pagamentos)
* Para cada endpoint, apresentar:
	* Método HTTP
	* Rota
	* Autenticação/permissões
	* Parâmetros
	* Exemplo de request/response
	* Códigos de status
	* Padrão de erro

1. Objetivo da etapa:
	* Descrever o contrato da API ("combinado" entre Front-end e Back-end), para que qualquer um consiga:
		* Entender o que cada endpoint faz
		* Saber o que enviar (request) e o que receber (response)
		* Validar regras e erros
		* Testar com Postman/Insomnia/Swagger
	* Prefira qualidade e clareza (melhor ter endpoint bem documentado que endpoint sem padrão)
2. Organização por recurso
	* Listar endpoints agrupando por "recurso"(módulo)
	* EX:
		* /auth (login, refresh, logout)
		* /usuarios (cadastro, perfil)
		* /unidades (listar unidades)
		* /produtos (CRUD, consulta)
		* /estoque (entradas/saídas, consulta por unidade)
		* /pedidos (criar pedido, status, consulta)
		* /pagamentos (simulação/mock, confirmação)
		* /fidelidade (pontos, saldo, histórico)
3. O que precisa apresentar em CADA endpoint? (checklist)
	* Nome do endpoint (propósito em 1 frase)
	* Método HTTP + rota
	* Autenticação e permissões
		* EX: JWT; papel ADMIN/GERENTE/CLIENTE)
	* Parâmetros
		* Path params (EX: /produtos/{id})
		* Query params (EX: ?page=1&limit=10)
	* Body (request) com exemplo JSON
	* Response (sucesso) com exemplo JSON
	* Códigos de status esperados (EX: 200, 201, 400, 401, 403, 404, 409, 422)
	* Padrão de erro (um JSON padrão para todas as falhas)
4. Regras mínimas (para evitar "API bagunçada)
	* URLs no plural --> /produtos, /pedidos
	* IDs no path --> /produtos/{id}
	* Paginação em listagens --> GET /produtos?page=1&limit=10
	* Status code coerente
		* 200 (ok), 201 (criado), 204 (sem conteúdo)
		* 400/422 (erro de validação), 401 (não autenticado), 403 (sem permissão)
		* 404 (não encontrado), 409 (conflito/regra de negócio)
	* Erro padronizado --> Sempre o mesmo formato JSON
5. Campos e padrões mínimos do contrato (OBRIGATÓRIO)
	* Em contratos de pedido, inclua EXPLICITAMENTE o campo canalPedido
	* Mantenha consistência de validação e erros
		* Se canalPedido não for informado, ou for inválido, API deve retornar erro com status apropriado (EX: 400/422) e mensagem padronizada

Exemplo de request:
```
{
	"canalPedido": "TOTEM",
	"clienteId":123,
	"itens":[
		{"produtoId":10, "quantidade":2}
	]
	"formaPagamento": "MOCK"
} 
```

Exemplo de filtro (listagem):

```GET /pedidos?canalPedido=APP&status=AGUARDANDO_PAGAMENTO```


## LGPD, Privacidade e Segurança no back-end (OBRIGATÓRIO)

* Deve estar explícita no back-end
* Quais dados pessoais são coletados
* Para qual finalidade
* Por qual base legal e como o consentimento é registrado
* Controles mínimos:
	* Hashing de senha
	* Autenticação por token
	* Autorização por perfil
	* Logs de acesso a dados sensíveis
	* Estratégia de retenção/anônimização (quando aplicável)

## Entrega Técnica (OBRIGATÓRIO)

* API funcional (rodando localmente) + dicumentação técnica completa que permita a correção e teste do sistema

1. Entregáveis obrigatórios