from __future__ import annotations

import datetime
from typing import Optional

def utc_now() -> datetime.datetime:
    return datetime.datetime.utcnow()

def isoformat(dt: Optional[datetime.datetime] = None) -> str:
    if dt is None:
        dt = utc_now()
    return dt.replace(microsecond=0).isoformat()
