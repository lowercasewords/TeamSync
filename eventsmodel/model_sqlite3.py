#Taka irizarry
#iriz@pdx.edu

# eventsmodel/model_sqlite3.py

import sqlite3
from pathlib import Path
from typing import List, Dict, Optional

DB_FILE = Path(__file__).resolve().parent.parent / "teamsync.db"


class EventModel:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._ensure_table()

    #Create table if not exists
    def _ensure_table(self) -> None:
        sql = """
        CREATE TABLE IF NOT EXISTS events (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            description TEXT,
            start_time  TEXT NOT NULL,
            end_time    TEXT NOT NULL,
            created_by  INTEGER,
            FOREIGN KEY (created_by) REFERENCES users(id)
        );
        """
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()

    #GET OPERATIONS

    #Return all events as list of dicts.
    def get_all_events(self) -> List[Dict]:
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT id, title, description, start_time, end_time, created_by
            FROM events
            ORDER BY start_time;
            """
        )
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    #Return a single event by id or none.
    def get_event_by_id(self, event_id: int) -> Optional[Dict]:
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT id, title, description, start_time, end_time, created_by
            FROM events
            WHERE id = ?;
            """,
            (event_id,),
        )
        row = cur.fetchone()
        return dict(row) if row else None

    #POST OPERATIONS

    #Insert a new event and return Id.
    def create_event(
        self,
        title: str,
        description: str,
        start_time: str,
        end_time: str,
        created_by: Optional[int] = None,
    ) -> int:

        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO events (title, description, start_time, end_time, created_by)
            VALUES (?, ?, ?, ?, ?);
            """,
            (title, description, start_time, end_time, created_by),
        )
        self.conn.commit()
        return cur.lastrowid

    #DELETE OPERATIONS

    #Delete event by id return true if deleted.
    def delete_event(self, event_id: int) -> bool:
        cur = self.conn.cursor()
        cur.execute("DELETE FROM events WHERE id = ?;", (event_id,))
        self.conn.commit()
        return cur.rowcount > 0
