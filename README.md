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
