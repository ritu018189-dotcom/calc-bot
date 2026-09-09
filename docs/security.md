# Security

## Bot token

`BOT_TOKEN` must come from an environment variable (or `.env`, which is
gitignored) — never hardcode it in source. If a real token is ever committed
to git history, treat it as compromised: revoke it via
[@BotFather](https://t.me/BotFather) (`/revoke` or `/token`) even after
removing it from the code, because git history keeps old commits around.

## The calculator (`/calc`)

`engines/math_engine.py` does **not** use Python's `eval()`. It parses the
expression into an AST and walks it itself, only ever calling a fixed
whitelist of operators (`+ - * / % **`) and functions (`sin`, `cos`, `tan`,
`sqrt`, `log`, `ln`) plus two constants (`pi`, `e`). Anything else — name
lookups, attribute access, function calls outside the whitelist — raises
before any code outside that whitelist runs. There is no code path from user
input back to Python's builtins.

## MFS payment verification (`/verify`)

`mfs_parser` parses the *text* of a pasted bKash/Nagad/Rocket message. It
does not call any provider API, so it cannot cryptographically prove a
message is genuine. Two safeguards exist:

1. **Replay protection** — `mfs_parser.store.TransactionStore` keeps a
   SQLite table of TrxIDs that have already been accepted, so the same
   confirmation text (e.g. a screenshot forwarded to two different sellers)
   can't be reused.
2. **Documented trust boundary** — the intended usage is to only feed this
   parser text that arrived through a channel you control (an SMS-forwarder
   app on the merchant's own registered phone, or a message forwarded from
   the official provider short code). A message *typed by a customer* is
   not proof of anything and should never be treated as payment confirmation
   on its own — always cross-check the parsed amount against the expected
   order total through your own records.

## Reporting a vulnerability

Open a private security advisory on the repository (GitHub → Security →
Advisories) rather than a public issue.
