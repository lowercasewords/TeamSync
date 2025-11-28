#Taka Irizarry (team member of TeamSync llc and charcuterie artist/educator/barista/software dev/musician/poet/gamer)
#iriz@pdx.edu
 
# entrymodel/model_sqlite3.py

import sqlite3
from pathlib import Path
from typing import List, Dict, Optional

DB_FILE = Path(__file__).resolve().parent.parent / "teamsync.db"


class UserModel:
    def __init__(self) -> None:
        #allow use from different threads
        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._ensure_table()

    #Create table if not exists
    def _ensure_table(self) -> None:
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            name  TEXT NOT NULL,
            role  TEXT NOT NULL CHECK(role IN ('read', 'write', 'admin'))
        );
        """
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()


    #GET OPERATORS

    #Return users as list of dicts
    def get_all_users(self) -> List[Dict]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, email, name, role FROM users ORDER BY id;")
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    #Return a user by email or none.
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT id, email, name, role FROM users WHERE email = ?;",
            (email,),
        )
        row = cur.fetchone()
        return dict(row) if row else None

    #POST OPERATIONS

    #Insert a new user and return id.
    #Error if email exists or role invalid
    def create_user(self, email: str, name: str, role: str = "read") -> int:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO users (email, name, role) VALUES (?, ?, ?);",
            (email, name, role),
        )
        self.conn.commit()
        return cur.lastrowid

    #DELETE OPERATIONS

    #Delete user by id. Returns true if deleted
    def delete_user_by_id(self, user_id: int) -> bool:
        cur = self.conn.cursor()
        cur.execute("DELETE FROM users WHERE id = ?;", (user_id,))
        self.conn.commit()
        return cur.rowcount > 0

    #Delete by email return true if deleted.
    def delete_user_by_email(self, email: str) -> bool:
        cur = self.conn.cursor()
        cur.execute("DELETE FROM users WHERE email = ?;", (email,))
        self.conn.commit()
        return cur.rowcount > 0

