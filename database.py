from contextlib import contextmanager
import sqlite3


database_url = "complaints.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(database_url)
    conn.row_factory = sqlite3.Row

    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """create table if not exists complaints(
id integer primary key autoincrement,
text text not null,
status text not null,
timestamp text not null,
sentiment text not null,
category text not null,
raw_result text not null
)
"""
        )

        conn.commit()

def save_complaint(complaint_data):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
insert into complaints (text, status, timestamp, sentiment, category, raw_result)
values (?, ?, ?, ?, ?, ?)
"""
        ,
        (
            complaint_data["text"],
            complaint_data["status"],
            complaint_data["timestamp"],
            complaint_data["sentiment"],
            complaint_data["category"],
            complaint_data["raw_result"],
        ))

        conn.commit()
        
        return cursor.lastrowid

def get_all_complaints():
    with get_db as conn:
        cursor = conn.cursor()
        cursor.execute("select * from complaints order by timestamp desc")
        
        return cursor.fetchall()

def get_complaint_by_id(complaint_id):
    with get_db as conn:
        cursor = conn.cursor()
        cursor.execute("select * from complaints where id = ?", (complaint_id))

        return cursor.fetchone()

def update_complaint_status(complaint_id, status):
    with get_db as conn:
        cursor = conn.cursor()
        cursor.execute("update complaints set status = ? where id = ?", (status, complaint_id))
        conn.commit()
        cursor.execute("select * from complaints where id = ?", (complaint_id))

        return cursor.fetchone()