# `/price`

```
/price <symbol>
```

Examples: `/price BTC-USD`, `/price AAPL`

Passes the symbol straight through to `yf.Ticker(symbol).history(...)`, so
anything Yahoo Finance recognizes works — stocks, ETFs, crypto pairs.
