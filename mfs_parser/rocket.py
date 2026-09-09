import re
from typing import Optional

from .base import ParsedTransaction

PROVIDER = "Rocket"

PATTERN = re.compile(
    r"you have received\s+(?:tk|taka)\s*(?P<amount>[\d,]+\.?\d*)"
    r".*?from\s+(?P<sender>\d{10,15})"
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
