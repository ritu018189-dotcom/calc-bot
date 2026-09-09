# `/convert`

```
/convert <amount> <from_code> <to_code>
```

Example: `/convert 100 USD BDT`

Fetches a live rate from Yahoo Finance (`engines/finance.py`), trying the FX
ticker form (`USDBDT=X`) then the crypto form (`BTC-USD`) if the first
returns no data. `<from_code>`/`<to_code>` don't need to exist in
`data/currencies/` — that only affects the flag/name shown, not whether a
rate can be found.

Errors:
- Wrong number of arguments → format reminder.
- Non-numeric amount → `Amount must be a number.`
- No rate found for the pair → `Invalid Currency Code or API Down.`
