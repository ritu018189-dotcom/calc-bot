# `/verify`

```
/verify <pasted payment confirmation message>
```

Example:
```
/verify You have received Tk 500.00 from 01712345678. Ref abc. Fee Tk 0.00.
Balance Tk 5,000.00. TrxID 8N7A6S5D4F at 10/10/2025 20:00
```

Parses a bKash/Nagad/Rocket confirmation message via `mfs_parser` and checks
the extracted TrxID against `mfs_parser.store.TransactionStore` (a SQLite
table of already-used TrxIDs) to prevent the same message being submitted
twice for two different orders.

**This does not verify the message against the provider** — see
[docs/security.md](../security.md) for the trust model and why you should
only feed it text from a channel you control.
