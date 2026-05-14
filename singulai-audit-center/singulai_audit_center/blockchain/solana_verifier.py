from __future__ import annotations

from typing import Optional

def verify_program_exists(program_id: str, rpc_endpoint: str) -> bool:
    """
    Stub para verificar se um programa Solana existe on-chain.
    Substituir por chamada real getAccountInfo via Solana RPC.
    """
    return True

def get_program_upgrade_authority(program_id: str, rpc_endpoint: str) -> Optional[str]:
    """
    Stub para obter autoridade de upgrade de um programa Solana.
    Retorna None para representar programa imutável ou não verificado.
    """
    return None

def verify_hash_on_chain(data_hash: str, program_id: str, rpc_endpoint: str) -> bool:
    """
    Stub para verificar hash registrado em programa Solana.
    """
    return False
