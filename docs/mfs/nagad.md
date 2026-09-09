# Nagad message format

`mfs_parser/nagad.py` matches messages shaped like:

```
Money Received. Amount: Tk 500.00. Sender: 01712345678. TxnID: ABC123XYZ.
Balance: Tk 1000.00. 10/10/2025 20:00
```

Captured fields: `amount` (after "Amount:"), `sender` (an 11-digit `01…`
number after "Sender:"), `trx_id` (after "TxnID:" or "TrxID:"). Comma
thousands separators in the amount (e.g. `12,500.50`) are stripped before
conversion to `float`.
