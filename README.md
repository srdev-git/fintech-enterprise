# 💳 Fintech Enterprise Worker

Projeto demonstrando uma arquitetura moderna de processamento de
transações, inspirado em boas práticas de engenharia de software e
arquitetura corporativa, com foco em escalabilidade, isolamento de
responsabilidades e resiliência.

------------------------------------------------------------------------

## 🧠 Visão Geral

Este projeto implementa um **worker assíncrono** para processamento de
transações financeiras utilizando:

-   🧠 Clean Architecture\
-   🧩 DDD (Domain-Driven Design) simplificado\
-   🧵 Worker assíncrono\
-   📬 AWS SQS (ou LocalStack para ambiente local)\
-   🗄 PostgreSQL\
-   🧪 Testes unitários com pytest\
-   🐳 Docker Ready

------------------------------------------------------------------------

## 📐 Arquitetura

    Worker (Infra)
       ↓
    Application Service (Use Case)
       ↓
    Domain
       ↓
    Repository Interface
       ↓
    Repository Implementation (SQLAlchemy)

### 🔹 Camadas

  Camada               Responsabilidade
  -------------------- ---------------------------------------
  **Domain**           Regras de negócio puras e entidades
  **Application**      Casos de uso e orquestração de regras
  **Infrastructure**   Banco de dados, ORM, mensageria (SQS)
  **Worker**           Orquestração e consumo de mensagens

------------------------------------------------------------------------

## 🚀 Tecnologias

-   Python 3.14+
-   SQLAlchemy
-   PostgreSQL
-   Boto3 (SQS)
-   Pytest
-   Docker / Docker Compose

------------------------------------------------------------------------

## 🐳 Executando com Docker

``` bash
docker compose up --build
```

Isso irá:

-   Subir PostgreSQL\
-   Subir LocalStack (SQS)\
-   Subir Worker\
-   Criar tabela automaticamente\
-   Criar fila automaticamente

------------------------------------------------------------------------

## 🧪 Executando testes

### Criar ambiente virtual

``` bash
py -m venv .venv
```

### Ativar

**Windows:**

``` bash
.\.venv\Scripts\Activate
```

**Linux/Mac:**

``` bash
source .venv/bin/activate
```

### Instalar dependências

``` bash
python -m pip install pytest pytest-cov
```

### Rodar testes

``` bash
pytest
```

### Rodar com cobertura

``` bash
pytest --cov=src --cov-report=term-missing
```

------------------------------------------------------------------------

## 🗂 Estrutura do Projeto

    src/
    ├── application/
    │   └── services/
    ├── domain/
    │   ├── entities/
    │   └── repositories/
    ├── infrastructure/
    │   ├── database/
    │   └── messaging/
    └── workers/

    tests/

------------------------------------------------------------------------

## 🔄 Fluxo de Processamento

1.  Mensagem chega no SQS\
2.  Worker consome mensagem\
3.  Application Service executa regra de negócio\
4.  Repository persiste no banco\
5.  Mensagem é removida da fila apenas após sucesso

------------------------------------------------------------------------

## 🛡 Práticas adotadas

-   Dependency Injection manual\
-   Repository Pattern\
-   Separação de camadas\
-   Testes unitários isolando infraestrutura\
-   Retry automático via `VisibilityTimeout` do SQS\
-   Idempotência via `external_id`

------------------------------------------------------------------------

## 📊 Exemplo de Payload

``` json
{
  "external_id": "abc123",
  "amount": 100
}
```

------------------------------------------------------------------------

## 🧠 Conceitos aplicados

-   Clean Architecture\
-   Hexagonal Architecture (Ports & Adapters)\
-   Domain-Driven Design (simplificado)\
-   Separation of Concerns\
-   Inversion of Control

------------------------------------------------------------------------

## 🎯 Próximos passos possíveis

-   Dead Letter Queue\
-   Outbox Pattern\
-   Observabilidade (Logs estruturados)\
-   CI/CD Pipeline\
-   Testcontainers\
-   Healthcheck do Worker

------------------------------------------------------------------------

## 👨‍💻 Autor

**Samuel Rocha**\
Arquiteto de Software

------------------------------------------------------------------------

## 📜 Licença

MIT
