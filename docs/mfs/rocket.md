# Rocket message format

`mfs_parser/rocket.py` matches messages shaped like:

```
You have received Tk 300.00 from 01812345678. Ref xyz. TxnID FK9284JD.
Balance Tk 800.00 at 10/10/2025 21:00
```

Similar to the bKash format, but the sender field accepts 10–15 digits
(Rocket account numbers aren't always the standard 11-digit mobile format),
and both "TxnID" and "TrxID" are accepted before the transaction id.

Because this pattern is close to bKash's, `mfs_parser`'s provider list tries
bKash first — a message that would match both is labeled bKash. In
practice real Rocket messages differ enough (they don't use the literal word
"TrxID" the way bKash does) that this hasn't been an issue; see
`tests/fixtures/rocket_valid.txt` for a message that's confirmed to reach
this parser specifically.
