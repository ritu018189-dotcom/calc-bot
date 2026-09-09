import os

from mfs_parser.bkash import parse

FIXTURES = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fixtures")


def _read(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as f:
        return f.read()


def test_parses_valid_bkash_message():
    txn = parse(_read("bkash_valid.txt"))
    assert txn is not None
    assert txn.provider == "bKash"
    assert txn.amount == 500.0
    assert txn.sender == "01712345678"
    assert txn.trx_id == "8N7A6S5D4F"


def test_message_without_trxid_does_not_match():
    assert parse(_read("bkash_missing_trxid.txt")) is None


def test_nagad_message_does_not_match_bkash_parser():
    assert parse(_read("nagad_valid.txt")) is None
