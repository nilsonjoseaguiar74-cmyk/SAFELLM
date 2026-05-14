from __future__ import annotations

import os
from typing import Any, Dict

def generate_pdf(report_data: Dict[str, Any], output_dir: str = "reports") -> str:
    """
    Stub de PDF.
    Em produção, substituir por ReportLab, WeasyPrint ou outro gerador real.
    """
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, f"report_{report_data.get('scan_id', 'unknown')}.pdf")

    content = f"SingulAI Audit Report\n\n{report_data}\n"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path

