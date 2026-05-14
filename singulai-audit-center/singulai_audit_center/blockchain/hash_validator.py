from __future__ import annotations

import hashlib
from typing import Union

def compute_sha256(data: Union[str, bytes]) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()

def verify_sha256(data: Union[str, bytes], expected_hash: str) -> bool:
    return compute_sha256(data) == expected_hash.lower()
