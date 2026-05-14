from __future__ import annotations

import asyncio
import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .database import async_session, engine, get_session
from .evidence.evidence_storage import save_evidence
from .models import Base, AuditEvidence, AuditFinding, AuditScan, AuditTarget, OnchainVerification
from .schemas import (
AuditScan as AuditScanSchema,
AuditScanCreate,
AuditTarget as AuditTargetSchema,
AuditTargetCreate,
ScanDetail,
)

app = FastAPI(
title="SingulAI Audit Center",
version="0.1.0",
description="Módulo independente de auditoria para integração segura com SingulAI Platform.",
)

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

@app.on_event("startup")
async def startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "service": "singulai-audit-center",
        "mode": "independent",
    }

@app.post("/targets", response_model=AuditTargetSchema, status_code=status.HTTP_201_CREATED)
async def create_target(
    target_in: AuditTargetCreate,
    session: AsyncSession = Depends(get_session),
) -> AuditTargetSchema:
    target = AuditTarget(
        name=target_in.name,
        target_type=target_in.target_type,
        value=target_in.value,
    )

    session.add(target)
    await session.commit()
    await session.refresh(target)

    return AuditTargetSchema.model_validate(target)

@app.get("/targets", response_model=List[AuditTargetSchema])
async def list_targets(session: AsyncSession = Depends(get_session)) -> list[AuditTargetSchema]:
    result = await session.scalars(select(AuditTarget).order_by(AuditTarget.id.desc()))
    return [AuditTargetSchema.model_validate(target) for target in result.all()]


@app.get("/scans", response_model=List[ScanDetail])
async def list_scans(session: AsyncSession = Depends(get_session)) -> list[ScanDetail]:
    query = (
        select(AuditScan)
        .order_by(AuditScan.id.desc())
        .options(
            selectinload(AuditScan.target),
            selectinload(AuditScan.findings),
            selectinload(AuditScan.evidence),
            selectinload(AuditScan.onchain_verifications),
        )
    )

    result = await session.scalars(query)

    return [ScanDetail.model_validate(scan) for scan in result.all()]


@app.post("/scans", response_model=AuditScanSchema, status_code=status.HTTP_201_CREATED)
async def create_scan(
    scan_in: AuditScanCreate,
    session: AsyncSession = Depends(get_session),
) -> AuditScanSchema:
    target = await session.get(AuditTarget, scan_in.target_id)

    if not target:
        raise HTTPException(status_code=404, detail="Target not found")

    scan = AuditScan(target_id=scan_in.target_id, status="pending")
    session.add(scan)

    await session.commit()
    await session.refresh(scan)

    asyncio.create_task(_perform_scan(scan.id))

    return AuditScanSchema.model_validate(scan)

@app.get("/scans/{scan_id}", response_model=ScanDetail)
async def get_scan_details(
    scan_id: int,
    session: AsyncSession = Depends(get_session),
) -> ScanDetail:
    query = (
        select(AuditScan)
        .where(AuditScan.id == scan_id)
        .options(
            selectinload(AuditScan.findings),
            selectinload(AuditScan.evidence),
            selectinload(AuditScan.onchain_verifications),
        )
    )

    result = await session.scalars(query)
    scan = result.first()

    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    return ScanDetail.model_validate(scan)
async def _perform_scan(scan_id: int) -> None:
    """
    Worker interno inicial.

    Este worker ainda é seguro e limitado.
    Não executa pentest real automaticamente.
    Gera uma evidência, um achado simulado e uma prova on-chain simulada.
    """
    async with async_session() as session:
        scan = await session.get(AuditScan, scan_id)

        if not scan:
            return

        scan.status = "running"
        await session.commit()

        await asyncio.sleep(2)

        content = f"SingulAI Audit Evidence - scan_id={scan.id}".encode("utf-8")
        file_name, file_path, sha = save_evidence(content)

        finding = AuditFinding(
            scan_id=scan.id,
            title="Initial audit placeholder",
            description=(
                "Auditoria inicial criada com sucesso. "
                "Este achado é simulado e serve para validar fluxo de banco, evidência e relatório."
            ),
            severity="info",
            recommendation="Conectar workers reais somente após validação do escopo autorizado.",
        )

        evidence = AuditEvidence(
            scan_id=scan.id,
            file_name=file_name,
            sha256=sha,
            storage_uri=file_path,
        )

        proof = OnchainVerification(
            scan_id=scan.id,
            chain="solana",
            tx_hash="0xDEADBEEF",
            proof_hash=sha,
            verified=False,
        )

        session.add(finding)
        session.add(evidence)
        session.add(proof)

        scan.completed_at = datetime.datetime.utcnow()
        scan.status = "completed"
        scan.risk_score = 10

        await session.commit()
