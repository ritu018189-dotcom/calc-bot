# `/calc`

```
/calc <expression>
```

Example: `/calc sin(90) + 10^2`

Evaluated by `engines/math_engine.py`, which parses the expression into an
AST and only allows: `+ - * / % **` (`^` is rewritten to `**`), the
functions `sin`, `cos`, `tan`, `sqrt`, `log` (base 10), `ln` (natural log),
and the constants `pi`, `e`. No `eval()` is used — see
[docs/security.md](../security.md).

Errors:
- Malformed expression → `Syntax Error`
- Division by zero → `♾️ Infinity`
- Anything outside the whitelist (function calls, name lookups, etc.) →
  `Disallowed expression`
