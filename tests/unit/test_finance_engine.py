from unittest.mock import MagicMock, patch

import pandas as pd

from engines.finance import YahooFinanceEngine


def _history_with_close(value):
    return pd.DataFrame({"Close": [value]})


def test_get_currency_rate_uses_fx_ticker_when_available():
    engine = YahooFinanceEngine()
    fake_ticker = MagicMock()
    fake_ticker.history.return_value = _history_with_close(121.5)

    with patch("engines.finance.yf.Ticker", return_value=fake_ticker) as ticker_cls:
        rate = engine.get_currency_rate("USD", "BDT")

    ticker_cls.assert_called_with("USDBDT=X")
    assert rate == 121.5


def test_get_currency_rate_falls_back_to_crypto_ticker():
    engine = YahooFinanceEngine()
    empty = pd.DataFrame()
    filled = _history_with_close(65000.0)

    fake_ticker = MagicMock()
    fake_ticker.history.side_effect = [empty, filled]

    with patch("engines.finance.yf.Ticker", return_value=fake_ticker):
        rate = engine.get_currency_rate("BTC", "USD")

    assert rate == 65000.0


def test_get_currency_rate_returns_none_when_both_lookups_empty():
    engine = YahooFinanceEngine()
    empty = pd.DataFrame()

    fake_ticker = MagicMock()
    fake_ticker.history.return_value = empty

    with patch("engines.finance.yf.Ticker", return_value=fake_ticker):
        rate = engine.get_currency_rate("XXX", "YYY")

    assert rate is None


def test_get_stock_price_returns_none_on_exception():
    engine = YahooFinanceEngine()
    with patch("engines.finance.yf.Ticker", side_effect=RuntimeError("network down")):
        assert engine.get_stock_price("AAPL") is None
