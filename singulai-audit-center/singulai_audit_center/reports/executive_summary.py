from __future__ import annotations

from typing import Any, Dict

def generate_summary(report_data: Dict[str, Any]) -> str:
    target = report_data.get("target_name", "Unknown target")
    risk = report_data.get("risk_score", "N/A")
    findings_count = len(report_data.get("findings", []))

    return (
        f"Executive Summary for {target}\n"
        f"Risk Score: {risk}\n"
        f"Number of Findings: {findings_count}\n\n"
        f"This audit assessed the security posture of {target} and "
        f"identified {findings_count} issue(s). See the full report for details."
    )

