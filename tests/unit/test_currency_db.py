from engines.currency_db import CURRENCY_DB, get_currency


def test_loads_more_than_150_currencies():
    assert len(CURRENCY_DB) > 150


def test_known_currency_has_expected_fields():
    usd = CURRENCY_DB["USD"]
    assert usd["name"] == "United States Dollar"
    assert usd["symbol"] == "$"
    assert usd["flag"]


def test_get_currency_is_case_insensitive():
    assert get_currency("usd")["code"] == "USD"


def test_get_currency_falls_back_for_unknown_code():
    fallback = get_currency("ZZZ")
    assert fallback["code"] == "ZZZ"
    assert fallback["flag"] == "🏳️"


def test_crypto_and_metal_entries_present():
    assert CURRENCY_DB["BTC"]["type"] == "Crypto"
    assert CURRENCY_DB["XAU"]["type"] == "Metal"
