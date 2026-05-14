# SingulAI Audit Center

Módulo independente de auditoria para integração segura com a SingulAI Platform.

Este módulo foi criado para operar de forma desacoplada do sistema principal. Ele possui banco próprio, API própria, workers próprios e camadas independentes para auditoria de infraestrutura, evidências, relatórios e verificação on-chain.

## Objetivo

Manter auditorias, scanners e verificações externas fora do core principal do SingulAI.

A integração com a plataforma principal deve ocorrer apenas por:

- API controlada
- banco de auditoria separado
- consulta somente leitura
- hashes e provas verificáveis

## Estrutura

```txt
singulai-audit-center/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── evidence/
├── logs/
├── reports/
└── singulai_audit_center/
    ├── main.py
    ├── database.py
    ├── models.py
    ├── schemas.py
    ├── blockchain/
    ├── evidence/
    ├── reports/
    └── workers/
````

## Princípio de isolamento

O Audit Center não deve modificar:

* usuários do sistema principal
* contratos principais
* carteiras principais
* dados financeiros
* dados sensíveis do core
* banco principal da plataforma

## Banco recomendado

```txt
singulai_audit_db
```

## Rodar localmente

```bash
cd singulai-audit-center
docker compose up --build
```

API:

```txt
http://localhost:8000
```

Documentação automática:

```txt
http://localhost:8000/docs
```

DEV - rodrigo.run © 2026 SingulAI - Todos os direitos reservados
