import sqlite3
import json

from models.entry import Entry

def get_all_entries():
    with sqlite3.connect("./dailyjournal.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.concept,
            a.entry,
            a.date,
            a.moodId
        FROM journalentries a
        """)

        entries = []

        dataset = db_cursor.fetchall()


        for row in dataset:

            entry = Entry(row['id'], row['concept'], row['entry'], row['date'], row['moodId'])

            entries.append(entry.__dict__)

    return json.dumps(entries)

def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.concept,
            a.entry,
            a.date,
            a.moodId
        FROM journalentries a
        WHERE a.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        entry = Entry(data['id'], data['concept'], data['entry'], data['date'], data['moodId'])

        return json.dumps(entry.__dict__)

def delete_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM journalentries
        WHERE id = ?
        """, (id, ))

def get_entries_by_search(term):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(f"""
        select
            c.id,
            c.concept,
            c.entry,
            c.date,
            c.moodId
        FROM journalentries c
        WHERE c.entry LIKE '%{term}%'
        """)

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'], row['date'], row['moodId'])
            entries.append(entry.__dict__)
    
    return json.dumps(entries)
