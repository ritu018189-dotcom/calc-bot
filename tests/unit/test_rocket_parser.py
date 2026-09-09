import os

from mfs_parser.rocket import parse

FIXTURES = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fixtures")


def _read(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as f:
        return f.read()


def test_parses_valid_rocket_message():
    txn = parse(_read("rocket_valid.txt"))
    assert txn is not None
    assert txn.provider == "Rocket"
    assert txn.amount == 300.0
    assert txn.trx_id == "FK9284JD"


def test_parses_comma_formatted_amount():
    txn = parse(_read("rocket_comma_amount.txt"))
    assert txn is not None
    assert txn.amount == 1750.25
    assert txn.trx_id == "RK55TT21"
