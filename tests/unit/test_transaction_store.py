import os

from mfs_parser import parse_mfs_message
from mfs_parser.store import TransactionStore

FIXTURES = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fixtures")


def _read(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as f:
        return f.read()


def test_blocks_replay_of_the_same_trx_id(tmp_path):
    db_path = str(tmp_path / "test_transactions.db")
    store = TransactionStore(db_path)
    try:
        txn = parse_mfs_message(_read("bkash_valid.txt"))
        assert not store.is_used(txn.trx_id)

        store.mark_used(txn)
        assert store.is_used(txn.trx_id)
    finally:
        store.close()


def test_persists_across_store_instances(tmp_path):
    db_path = str(tmp_path / "test_transactions.db")
    txn = parse_mfs_message(_read("nagad_valid.txt"))

    store = TransactionStore(db_path)
    store.mark_used(txn)
    store.close()

    reopened = TransactionStore(db_path)
    try:
        assert reopened.is_used(txn.trx_id)
    finally:
        reopened.close()


def test_different_trx_ids_are_independent(tmp_path):
    db_path = str(tmp_path / "test_transactions.db")
    store = TransactionStore(db_path)
    try:
        bkash_txn = parse_mfs_message(_read("bkash_valid.txt"))
        rocket_txn = parse_mfs_message(_read("rocket_valid.txt"))

        store.mark_used(bkash_txn)
        assert store.is_used(bkash_txn.trx_id)
        assert not store.is_used(rocket_txn.trx_id)
    finally:
        store.close()
