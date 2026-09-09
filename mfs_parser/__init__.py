"""
Parser + replay-guard for Bangladeshi Mobile Financial Service (MFS)
transaction confirmation messages (bKash, Nagad, Rocket).

IMPORTANT — trust model:
This package extracts structured fields (amount, sender, TrxID) out of a
message's *text*. It does not call any bKash/Nagad/Rocket API and cannot
prove the message actually originated from the provider. Treat it as a
convenience parser, not a source of truth — see docs/security.md.

Adding a new provider is a matter of dropping a `parse(text) -> ParsedTransaction
| None` module next to bkash.py/nagad.py/rocket.py and registering it in
_PROVIDERS below. See docs/guides/adding_an_mfs_provider.md.
"""

from typing import Optional

from . import bkash, nagad, rocket
from .base import ParsedTransaction
from .store import TransactionStore

_PROVIDERS = [bkash, nagad, rocket]


def parse_mfs_message(text: str) -> Optional[ParsedTransaction]:
    """Try each known provider parser against the text; return the first match."""
    for provider_module in _PROVIDERS:
        result = provider_module.parse(text)
        if result:
            return result
    return None


__all__ = ["parse_mfs_message", "ParsedTransaction", "TransactionStore"]
