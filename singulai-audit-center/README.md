# SingulAI Audit Center

Módulo independente de auditoria, evidências e verificação on-chain para integração segura com a SingulAI Platform.

O SingulAI Audit Center foi criado para operar separado do sistema principal. Ele possui API própria, banco próprio, workers próprios, storage de evidências e camadas separadas para auditoria de infraestrutura, blockchain, relatórios e integração futura com IA local.

## Objetivo

Manter auditorias, scanners, verificações externas e processos sensíveis fora do core principal do SingulAI.

A integração com a plataforma principal deve ocorrer apenas por API controlada, banco de auditoria separado, consulta somente leitura, hashes de evidências e provas on-chain.

## Princípio de isolamento

O Audit Center não deve modificar:

- usuários do sistema principal
- contratos principais
- carteiras principais
- dados financeiros
- dados sensíveis do core
- banco principal da plataforma
- regras de execução da SingulAI Platform

A SingulAI Platform pode consumir resultados da auditoria, mas não deve executar scanners diretamente.

## Arquitetura

```txt
SingulAI Platform
        |
        | consulta segura
        v
Audit Client / API controlada
        |
        v
SingulAI Audit Center
        |
        |-- API propria
        |-- Banco proprio
        |-- Workers de auditoria
        |-- Evidencias SHA-256
        |-- Relatorios
        |-- Verificacao on-chain
        |-- Integracao futura com IA local
```

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
```

## Stack inicial

* FastAPI
* PostgreSQL
* SQLAlchemy Async
* Docker
* Docker Compose
* Python async workers
* Evidências com SHA-256
* Stubs Solana/EVM
* Relatórios JSON/PDF

## Banco de dados

Banco recomendado:

```txt
singulai_audit_db
```

Credenciais padrão de desenvolvimento:

```txt
POSTGRES_DB=singulai_audit_db
POSTGRES_USER=audit_user
POSTGRES_PASSWORD=audit_pass
```

Em produção, mover essas credenciais para `.env` e substituir por senhas fortes.

## Tabelas principais

* audit_targets
* audit_scans
* audit_findings
* audit_evidence
* onchain_verifications

## Rotas iniciais da API

Health check:

```http
GET /health
```

Criar alvo:

```http
POST /targets
```

Body exemplo:

```json
{
  "name": "singulai.site",
  "target_type": "domain",
  "value": "singulai.site"
}
```

Listar alvos:

```http
GET /targets
```

Criar auditoria:

```http
POST /scans
```

Body exemplo:

```json
{
  "target_id": 1
}
```

Consultar auditoria:

```http
GET /scans/{scan_id}
```

## Fluxo inicial de auditoria

```txt
1. Cadastra alvo autorizado
2. Cria auditoria
3. Aciona worker interno
4. Gera evidência simulada
5. Calcula SHA-256
6. Salva achado informativo
7. Cria prova on-chain simulada
8. Finaliza scan
```

A versão inicial é propositalmente limitada. Scanners reais só devem ser conectados depois de validação de escopo, autorização e segurança.

## Evidências

Fluxo recomendado:

```txt
conteúdo bruto
    ↓
arquivo local
    ↓
hash SHA-256
    ↓
registro no banco
    ↓
prova on-chain futura
```

## Verificação on-chain

A camada blockchain está preparada para evoluir para validações reais.

Solana:

* verificar se programa existe
* verificar autoridade de upgrade
* verificar hash registrado
* validar provas de execução

EVM:

* verificar se contrato existe
* consultar owner
* consultar bytecode
* verificar hash registrado
* detectar contrato proxy/upgradeable

## Smart contract futuro

A integração futura recomendada é por um contrato `AuditProofRegistry`.

O contrato não deve armazenar relatórios completos. Ele deve registrar apenas hashes e metadados essenciais:

```solidity
struct AuditProof {
    bytes32 auditId;
    bytes32 targetHash;
    bytes32 reportHash;
    bytes32 evidenceHash;
    address auditor;
    uint256 timestamp;
    uint8 riskScore;
    bool valid;
}
```

Funções previstas:

* registerAuditProof()
* verifyAuditProof()
* revokeAuditProof()
* getAuditProof()
* isAuditValid()

## Workers

Os workers ficam em:

```txt
singulai_audit_center/workers/
```

O worker inicial é:

```txt
infra_scan_worker.py
```

No futuro, pode encapsular:

* Nmap
* Nikto
* WhatWeb
* Curl
* SSL checks
* DNS checks
* validações de headers
* METATRON adapter

## Segurança operacional

Antes de ativar scanners reais:

* exigir autorização explícita do alvo
* registrar escopo
* limitar rate
* criar fila de execução
* impedir scans fora da allowlist
* auditar quem iniciou cada scan
* separar logs por execução
* limitar CPU/RAM
* impedir execução dentro do core principal

## Rodar localmente

```bash
cd singulai-audit-center
docker compose up --build
```

API local:

```txt
http://localhost:8000
```

Swagger/OpenAPI:

```txt
http://localhost:8000/docs
```

Health check:

```txt
http://localhost:8000/health
```

## Validação

Validar Python:

```bash
python -m py_compile $(find singulai-audit-center/singulai_audit_center -name "*.py")
```

Validar Docker Compose:

```bash
cd singulai-audit-center
docker compose config
```
```

## Próximas fases

Fase 1:

* validar API
* validar banco
* validar containers
* testar criação de alvo
* testar criação de scan
* testar leitura de resultado

Fase 2:

* criar integração com dashboard
* criar client somente leitura
* criar autenticação interna
* criar score de risco real

Fase 3:

* conectar Solana RPC
* conectar EVM RPC
* criar AuditProofRegistry
* registrar hashes on-chain

Fase 4:

* integrar Ollama
* interpretar achados
* gerar relatório executivo
* gerar recomendações técnicas

Fase 5:

* integrar scanners reais
* criar allowlist obrigatória
* criar fila de execução
* criar rate limit
* criar painel SOC/Audit Center

## Regra final

A SingulAI Platform deve consumir o Audit Center como fonte externa de verdade auditável.

O core principal não deve executar scanners, manipular evidências brutas ou depender diretamente de ferramentas ofensivas.

## Licença

Proprietary / Internal Development

Todos os direitos reservados.

DEV - rodrigo.run © 2026 SingulAI - Todos os direitos reservados
