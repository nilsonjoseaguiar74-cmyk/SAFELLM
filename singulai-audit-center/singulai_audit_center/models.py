from __future__ import annotations

import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()

class AuditTarget(Base):
    __tablename__ = "audit_targets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    target_type: Mapped[str] = mapped_column(String(50), nullable=False)
    value: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.utcnow,
    )

    scans: Mapped[list["AuditScan"]] = relationship(
        "AuditScan",
        back_populates="target",
        cascade="all, delete-orphan",
    )

class AuditScan(Base):
    __tablename__ = "audit_scans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    target_id: Mapped[int] = mapped_column(Integer, ForeignKey("audit_targets.id"), nullable=False)
    started_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.utcnow,
    )
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    risk_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    target: Mapped["AuditTarget"] = relationship("AuditTarget", back_populates="scans")
    findings: Mapped[list["AuditFinding"]] = relationship(
        "AuditFinding",
        back_populates="scan",
        cascade="all, delete-orphan",
    )
    evidence: Mapped[list["AuditEvidence"]] = relationship(
        "AuditEvidence",
        back_populates="scan",
        cascade="all, delete-orphan",
    )
    onchain_verifications: Mapped[list["OnchainVerification"]] = relationship(
        "OnchainVerification",
        back_populates="scan",
        cascade="all, delete-orphan",
    )

class AuditFinding(Base):
    __tablename__ = "audit_findings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    scan_id: Mapped[int] = mapped_column(Integer, ForeignKey("audit_scans.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False)
    recommendation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    scan: Mapped["AuditScan"] = relationship("AuditScan", back_populates="findings")

class AuditEvidence(Base):
    __tablename__ = "audit_evidence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    scan_id: Mapped[int] = mapped_column(Integer, ForeignKey("audit_scans.id"), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.utcnow,
    )
    storage_uri: Mapped[str] = mapped_column(String(512), nullable=False)

    scan: Mapped["AuditScan"] = relationship("AuditScan", back_populates="evidence")

class OnchainVerification(Base):
    __tablename__ = "onchain_verifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    scan_id: Mapped[int] = mapped_column(Integer, ForeignKey("audit_scans.id"), nullable=False)
    chain: Mapped[str] = mapped_column(String(50), nullable=False)
    tx_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    proof_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.utcnow,
    )

    scan: Mapped["AuditScan"] = relationship("AuditScan", back_populates="onchain_verifications")

