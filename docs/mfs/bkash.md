# bKash message format

`mfs_parser/bkash.py` matches messages shaped like:

```
You have received Tk 500.00 from 01712345678. Ref abc. Fee Tk 0.00.
Balance Tk 5,000.00. TrxID 8N7A6S5D4F at 10/10/2025 20:00
```

Captured fields: `amount` (after "Tk"/"Taka"), `sender` (an 11-digit `01…`
number after "from"), `trx_id` (alphanumeric, after "TrxID"). Matching is
case-insensitive and tolerant of line breaks between fields.

If bKash changes their message wording, update the regex in
`mfs_parser/bkash.py` and add the new format as a fixture under
`tests/fixtures/` so a regression is caught by `tests/unit/test_bkash_parser.py`.
