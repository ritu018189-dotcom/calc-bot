"""
Regression tests for message shapes that must NOT be treated as an incoming
payment — the main risk being an outgoing "sent" confirmation (which proves
nothing about money received) getting matched by mistake.
"""

import os

from mfs_parser import parse_mfs_message

FIXTURES = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fixtures")


def _read(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as f:
        return f.read()


def test_outgoing_bkash_message_is_not_treated_as_received():
    assert parse_mfs_message(_read("bkash_sent_not_received.txt")) is None
