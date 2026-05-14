from __future__ import annotations

from typing import Tuple

def write_proof_to_chain(
    chain: str,
    data_hash: str,
    identifier: str,
    rpc_endpoint: str,
    **kwargs,
) -> Tuple[str, bool]:
    """
    Stub de escrita de prova on-chain.
    Retorna tx_hash falso e sucesso False até a integração real.
    """
    return "0xDEADBEEF", False
