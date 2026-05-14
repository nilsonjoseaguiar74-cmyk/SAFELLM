from __future__ import annotations

import os
from typing import Tuple

from .sha256_service import hash_file
from .timestamp_service import isoformat

def save_evidence(content: bytes, evidence_dir: str = "evidence") -> Tuple[str, str, str]:
    os.makedirs(evidence_dir, exist_ok=True)

    timestamp = isoformat().replace(":", "-").replace("T", "_")
    file_name = f"evidence_{timestamp}.bin"
    file_path = os.path.join(os.getcwd(), evidence_dir, file_name)

    with open(file_path, "wb") as f:
        f.write(content)

    sha = hash_file(file_path)

    return file_name, file_path, sha

