from __future__ import annotations

from typing import Optional

from .evm_verifier import get_contract_owner
from .solana_verifier import get_program_upgrade_authority

def get_upgrade_authority(
    chain: str,
    identifier: str,
    rpc_endpoint: str,
    abi: Optional[dict] = None,
) -> Optional[str]:
    chain = chain.lower()

    if chain == "solana":
        return get_program_upgrade_authority(identifier, rpc_endpoint)

    if chain in ("ethereum", "evm", "polygon", "bsc"):
        if abi is None:
            return None
        return get_contract_owner(identifier, abi, rpc_endpoint)

    return None

