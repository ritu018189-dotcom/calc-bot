import re
from typing import Optional

from .base import ParsedTransaction

PROVIDER = "Nagad"

PATTERN = re.compile(
    r"(?:money received|received)\s*\.?\s*amount[:\s]+(?:tk|taka)\s*(?P<amount>[\d,]+\.?\d*)"
    r".*?sender[:\s]+(?P<sender>01\d{9})"
    r".*?(?:txnid|trxid)[:\s]+(?P<trx_id>[A-Z0-9]+)",
    re.IGNORECASE | re.DOTALL,
)


def parse(text: str) -> Optional[ParsedTransaction]:
    match = PATTERN.search(text)
    if not match:
        return None
    return ParsedTransaction(
        provider=PROVIDER,
        amount=float(match.group("amount").replace(",", "")),
        sender=match.group("sender"),
        trx_id=match.group("trx_id").upper(),
        raw_text=text,
    )
