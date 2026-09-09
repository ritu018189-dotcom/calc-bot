import sqlite3
import time

from .base import ParsedTransaction


class TransactionStore:
    """
    Tracks TrxIDs that have already been accepted, so the same confirmation
    message can't be submitted twice for two different orders.
    """

    def __init__(self, db_path: str = "verified_transactions.db") -> None:
        self._conn = sqlite3.connect(db_path)
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS used_transactions (
                trx_id TEXT PRIMARY KEY,
                provider TEXT NOT NULL,
                amount REAL NOT NULL,
                sender TEXT,
                verified_at INTEGER NOT NULL
            )
            """)
        self._conn.commit()

    def is_used(self, trx_id: str) -> bool:
        cur = self._conn.execute(
            "SELECT 1 FROM used_transactions WHERE trx_id = ?", (trx_id,)
        )
        return cur.fetchone() is not None

    def mark_used(self, txn: ParsedTransaction) -> None:
        self._conn.execute(
            "INSERT INTO used_transactions (trx_id, provider, amount, sender, verified_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (txn.trx_id, txn.provider, txn.amount, txn.sender, int(time.time())),
        )
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()
