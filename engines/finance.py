"""Wraps Yahoo Finance lookups for currency pairs and stock/crypto tickers."""

import logging
from typing import Optional

import yfinance as yf

logger = logging.getLogger("calc_bot.finance")


class YahooFinanceEngine:
    """Provides real-time data for currencies, stocks, and crypto via yfinance."""

    def get_currency_rate(self, base: str, target: str) -> Optional[float]:
        """Fetch a live exchange rate, trying FX-ticker then crypto-ticker form."""
        try:
            ticker1 = f"{base}{target}=X"
            data = yf.Ticker(ticker1).history(period="1d")
            if not data.empty:
                return data["Close"].iloc[-1]

            ticker2 = f"{base}-{target}"
            data2 = yf.Ticker(ticker2).history(period="1d")
            if not data2.empty:
                return data2["Close"].iloc[-1]

            return None
        except Exception as e:
            logger.error(f"Currency API Error: {e}")
            return None

    def get_stock_price(self, symbol: str) -> Optional[float]:
        """Fetch the latest close price for a stock/crypto ticker."""
        try:
            data = yf.Ticker(symbol).history(period="1d")
            if not data.empty:
                return data["Close"].iloc[-1]
            return None
        except Exception as e:
            logger.error(f"Price API Error: {e}")
            return None
