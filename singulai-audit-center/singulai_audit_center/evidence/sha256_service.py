from __future__ import annotations

from typing import Union

from ..blockchain.hash_validator import compute_sha256

def hash_data(data: Union[str, bytes]) -> str:
    return compute_sha256(data)

def hash_file(file_path: str) -> str:
    with open(file_path, "rb") as f:
        return compute_sha256(f.read())
