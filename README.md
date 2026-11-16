# 🧠 Jogo da Memória Serverless na AWS

Aplicação web interativa desenvolvida e implantada com arquitetura **100% Serverless na AWS** (Região `sa-east-1` - São Paulo), integrando hospedagem estática, API REST gerenciada, computação orientada a eventos e banco de dados NoSQL de baixa latência.

---

## 🏗️ Arquitetura da Solução

```text
[ Navegador (Cliente) ]
       │
       ├──► GET (HTML/CSS/JS) ──► [ Amazon S3 (Static Website Hosting) ]
       │
       └──► HTTPS (REST API)  ──► [ Amazon API Gateway (Regional /prod) ]
                                          │
                                          ▼ (Lambda Proxy Integration)
                                  [ AWS Lambda (Python 3.12) ]
                                          │
                                          ├──► IAM Role (Princípio do Menor Privilégio)
                                          │
                                          ▼ (boto3 SDK)
                                  [ Amazon DynamoDB (On-Demand) ]
```

---

## 🛠️ Serviços AWS Utilizados

* **Amazon S3:** Hospedagem de site estático (*Static Website Hosting*) com política de bucket para leitura pública (`s3:GetObject`) entregando o frontend em HTML5, CSS3 e JavaScript puro.
* **Amazon API Gateway:** API REST Regional (`prod`) com suporte a **CORS** e **Integração de Proxy do Lambda** expondo três endpoints:
  * `POST /resultado` — Registra a pontuação, tentativas e tempo da partida.
  * `GET /ranking` — Consulta e ordena o Top 10 melhores pontuações.
  * `GET /jogador/{nome}` — Busca o histórico de partidas de um jogador específico usando parâmetro de caminho dinâmico.
* **AWS Lambda:** Função em **Python 3.12** utilizando `boto3` para validação de payload, geração de identificadores (`UUIDv4` e hash `MD5` para `playerId`) e operações no DynamoDB.
* **Amazon DynamoDB:** Tabela NoSQL em modo **On-Demand** utilizando chave primária composta:
  * **Partition Key (`playerId`):** Hash MD5 do nome do jogador (distribuição uniforme de partições).
  * **Sort Key (`gameId`):** UUID único da partida (permite múltiplas partidas por jogador e consultas eficientes via `Query`).
* **AWS IAM:** Role de execução dedicada com política em linha restrita apenas às ações necessárias (`dynamodb:PutItem`, `dynamodb:GetItem`, `dynamodb:Scan`, `dynamodb:Query`) sobre a tabela específica do projeto, além do envio de logs ao **Amazon CloudWatch**.

---

## 📸 Evidências da Implantação

* **Tabela NoSQL (Amazon DynamoDB):** [`Docs/DynamoDB- Pint 1.png`](Docs/DynamoDB-%20Pint%201.png)
* **Backend Serverless (AWS Lambda):** [`Docs/Teste Lambda 02.png`](Docs/Teste%20Lambda%2002.png)
* **Endpoints REST (Amazon API Gateway):** [`Docs/API Gateway_02.png`](Docs/API%20Gateway_02.png)
* **Hospedagem Estática (Amazon S3):** [`Docs/memory-game-lab-vagner-santos_final.png`](Docs/memory-game-lab-vagner-santos_final.png)

---

## 🐛 Troubleshooting & Lições Aprendidas na Prática

Durante a implantação e os testes de integração ponta a ponta, foram diagnosticados e resolvidos pontos críticos reais de arquitetura:
1. **Permissões IAM (Least Privilege):** Correção de erro `AccessDeniedException` ao vincular a IAM Role customizada à função Lambda no lugar da role padrão de execução.
2. **Integração Proxy & CORS:** Configuração explícita de cabeçalhos `Access-Control-Allow-Origin` tanto no API Gateway (métodos `OPTIONS`) quanto nas respostas JSON retornadas pelo Lambda.
3. **Configuração Frontend x Backend:** Sincronização do endpoint de produção do API Gateway no arquivo `js/config.js` e controle de cache do navegador durante atualizações de artefatos estáticos no S3.
4. **Governança de Custos:** Desprovisionamento ordenado de todos os recursos (S3, API Gateway, Lambda, CloudWatch Logs, DynamoDB e IAM Role) após a validação e coleta de evidências.

---

## 📁 Estrutura do Projeto

```text
├── Docs/            # Evidências de arquitetura e implantação na AWS
├── assets/          # Recursos estáticos
├── css/             # Estilização da interface (style.css)
├── js/              # Lógica do jogo (game.js) e endpoint da API (config.js)
├── lambda/          # Código fonte da função serverless (lambda_function.py)
└── index.html       # Página principal da aplicação
```
