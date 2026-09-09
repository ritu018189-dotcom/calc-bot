import os

from mfs_parser import parse_mfs_message

FIXTURES = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fixtures")


def _read(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as f:
        return f.read()


def test_router_picks_correct_provider_for_each_fixture():
    assert parse_mfs_message(_read("bkash_valid.txt")).provider == "bKash"
    assert parse_mfs_message(_read("nagad_valid.txt")).provider == "Nagad"
    assert parse_mfs_message(_read("rocket_valid.txt")).provider == "Rocket"


def test_router_returns_none_for_unrecognized_text():
    assert parse_mfs_message(_read("unrecognized.txt")) is None
