from __future__ import annotations

import asyncio
from typing import Any, Dict

async def run_port_scan(host: str) -> Dict[str, Any]:
    """
    Worker stub para scan de portas.
    Futuramente deve encapsular nmap com controle de escopo e autorização.
    """
    await asyncio.sleep(1)

    return {
        "target": host,
        "open_ports": [80, 443],
        "services": {
            80: "http",
            443: "https",
        },
    }

async def run_web_scan(url: str) -> Dict[str, Any]:
    """
    Worker stub para scanner web.
    Futuramente pode integrar WhatWeb, Nikto, curl e validações próprias.
    """
    await asyncio.sleep(1)

    return {
        "target": url,
        "server": "stub-server",
        "frameworks": [],
        "cve_count": 0,
    }