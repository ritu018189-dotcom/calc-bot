from dataclasses import dataclass
from typing import Optional


@dataclass
class ParsedTransaction:
    provider: str
    amount: float
    sender: Optional[str]
    trx_id: str
    raw_text: str
