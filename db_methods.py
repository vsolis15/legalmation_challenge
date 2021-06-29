from db import get_db


def insert_file(name, defendants, plaintiffs):
    db = get_db()
    cursor = db.cursor()
    statement = "INSERT INTO files(name, defendants, plaintiffs) VALUES (?, ?, ?)"
    cursor.execute(statement, [name, defendants, plaintiffs])
    db.commit()
    return True

def get_files():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT id, name, defendants, plaintiffs FROM files"
    cursor.execute(query)
    return cursor.fetchall()

def get_file_by_id(id):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, name, defendants, plaintiffs FROM files WHERE id = ?"
    cursor.execute(statement, [id])
    return cursor.fetchone()

def get_file_by_name(name):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, name, defendants, plaintiffs FROM files WHERE name = ?"
    cursor.execute(statement, [name])
    return cursor.fetchone()