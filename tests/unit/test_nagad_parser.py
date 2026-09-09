import os

from mfs_parser.nagad import parse

FIXTURES = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fixtures")


def _read(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as f:
        return f.read()


def test_parses_valid_nagad_message():
    txn = parse(_read("nagad_valid.txt"))
    assert txn is not None
    assert txn.provider == "Nagad"
    assert txn.amount == 500.0
    assert txn.sender == "01712345678"
    assert txn.trx_id == "ABC123XYZ"


def test_parses_lowercase_and_comma_amount():
    txn = parse(_read("nagad_large_amount.txt"))
    assert txn is not None
    assert txn.amount == 12500.50
    assert txn.trx_id == "XYZ987654"


def test_bkash_message_does_not_match_nagad_parser():
    assert parse(_read("bkash_valid.txt")) is None
