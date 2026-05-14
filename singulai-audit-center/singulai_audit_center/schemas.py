from __future__ import annotations

import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class AuditTargetBase(BaseModel):
    name: str = Field(..., examples=["singulai.site"])
    target_type: str = Field(..., examples=["domain"])
    value: str = Field(..., examples=["singulai.site"])

class AuditTargetCreate(AuditTargetBase):
    pass

class AuditTarget(AuditTargetBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime.datetime

class AuditScanCreate(BaseModel):
    target_id: int

class AuditScan(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    target_id: int
    started_at: datetime.datetime
    completed_at: Optional[datetime.datetime]
    status: str
    risk_score: Optional[int]

class AuditFinding(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    scan_id: int
    title: str
    description: str
    severity: str
    recommendation: Optional[str]

class AuditEvidence(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    scan_id: int
    file_name: str
    sha256: str
    timestamp: datetime.datetime
    storage_uri: str

class OnchainVerification(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    scan_id: int
    chain: str
    tx_hash: str
    proof_hash: str
    verified: bool
    timestamp: datetime.datetime

class ScanDetail(AuditScan):
    target: Optional[AuditTarget] = None
    findings: list[AuditFinding] = []
    evidence: list[AuditEvidence] = []
    onchain_verifications: list[OnchainVerification] = []
