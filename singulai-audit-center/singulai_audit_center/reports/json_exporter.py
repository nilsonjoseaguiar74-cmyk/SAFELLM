from __future__ import annotations

import json
import os
from typing import Any, Dict

def export_to_json(data: Dict[str, Any], output_dir: str = "reports") -> str:
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, f"report_{data.get('scan_id', 'unknown')}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)

    return file_path

