# Adding an MFS provider

`mfs_parser` tries one parser module per provider, in the order listed in
`mfs_parser/__init__.py`'s `_PROVIDERS`, and returns the first match.

To add a new provider (e.g. Upay):

1. Create `mfs_parser/upay.py`:

   ```python
   import re
   from .base import ParsedTransaction

   PROVIDER = "Upay"

   PATTERN = re.compile(
       r"...",  # named groups: amount, sender (optional), trx_id
       re.IGNORECASE | re.DOTALL,
   )

   def parse(text: str):
       match = PATTERN.search(text)
       if not match:
           return None
       return ParsedTransaction(
           provider=PROVIDER,
           amount=float(match.group("amount").replace(",", "")),
           sender=match.groupdict().get("sender"),
           trx_id=match.group("trx_id").upper(),
           raw_text=text,
       )
   ```

2. Register it in `mfs_parser/__init__.py`:

   ```python
   from . import bkash, nagad, rocket, upay
   _PROVIDERS = [bkash, nagad, rocket, upay]
   ```

3. Add fixtures under `tests/fixtures/` (a valid message and, if the
   provider's format has known edge cases, one or two malformed ones) and a
   `tests/unit/test_upay_parser.py` mirroring the existing provider tests.

Keep provider patterns as specific as possible — a pattern that's too loose
can shadow a later provider's messages if it happens to match first.
