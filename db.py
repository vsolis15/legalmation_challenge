import sqlite3
DATABASE_NAME = "files.db"


def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


def create_tables():
    tables = [
        """CREATE TABLE IF NOT EXISTS files(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
				defendants TEXT NOT NULL,
				plaintiffs TEXT NOT NULL
            )
        """
    ]
    db = get_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)