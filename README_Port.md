# 📚 Academic Flow API

API RESTful central da plataforma **Academic Flow**, responsável por autenticação, gestão acadêmica e integração do sistema educacional da UFSJ.

---

## 📌 Visão Geral

A **Academic Flow API** é o núcleo backend reutilizável de todos os projetos da plataforma Academic Flow.
Ela fornece endpoints seguros, padronizados e escaláveis para aplicações acadêmicas, permitindo o gerenciamento completo de dados educacionais.

### Objetivos do Projeto

- Centralizar regras e dados acadêmicos
- Facilitar integração com aplicações frontend
- Garantir segurança e integridade das informações
- Permitir expansão modular para novos recursos

---

## 🚀 Tecnologias Utilizadas

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **JWT (Access Token e Refresh Token)**
- **PostgreSQL**
- **Docker**
- **Swagger / OpenAPI**

---

## 📂 Estrutura do Projeto

```
Academic-Flow-API/
├── backend/
│   ├── api/
│   ├── config/
│   ├── data/
│   ├── data_store/
│   ├── ml/
│   ├── core/
│   ├── models/
│   ├── libs/
│   └── main.py
├── Dockerfile
├── requirements.txt
├── run.sh
├── pyproject.toml
├── LICENSE
├── README.md
└── SECURITY.md
```

---

## 🔐 Autenticação

A API utiliza JWT com Access Token e Refresh Token.

Header obrigatório:

```
Authorization: Bearer <access_token>
```

---

## 📘 Documentação da API

Swagger:

- https://academic-flow-api.onrender.com/docs

---

## 🐳 Docker

```
docker build -t academic-flow-api .
docker run -p 8000:8000 academic-flow-api
```

---

## 🚀 Deploy

```
./run.sh
```

---

## 📜 Licença

Este projeto é licenciado sob a **GNU General Public License v3.0 (GPL-3.0)**.

Você pode:

- Usar
- Estudar
- Modificar
- Redistribuir

Desde que **qualquer versão derivada também seja distribuída sob a GPL v3**.

Veja o arquivo [LICENSE](./LICENSE) para mais detalhes.
