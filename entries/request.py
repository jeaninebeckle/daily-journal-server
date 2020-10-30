import sqlite3
import json

from models.entry import Entry
from models.mood import Mood
from models.tag import Tag

def get_all_entries():
    with sqlite3.connect("./dailyjournal.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            j.id,
            j.concept,
            j.entry,
            j.date,
            j.moodId,
            m.label mood_label
        FROM journalentries j
        JOIN moods m
            ON m.id = j.moodId
        """)

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            entry = Entry(row['id'], row['concept'], row['entry'], row['date'], row['moodId'])

            mood = Mood(row['moodId'], row['mood_label'])

            entry.mood = mood.__dict__
            
            entries.append(entry.__dict__)

            db_cursor.execute("""
            SELECT
                t.id,
                t.name,
                e.tag_id
            FROM tags t
            JOIN entrytags e
                ON t.id = e.tag_id
            WHERE e.entry_id = ?
            """, (row['id'], ))

            tagset = db_cursor.fetchall()
            tags = []
            for tag in tagset:
                each_tag = Tag(tag['id'], tag['name'])
                tags.append(each_tag.__dict__)
            entry.tags = tags

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

def create_journal_entry(new_entry):
    print(new_entry)
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()
        #a list is brackets, like an array in JS

        db_cursor.execute("""
        INSERT INTO journalentries
            ( concept, entry, date, moodId )
        VALUES
            ( ?, ?, ?, ?);
        """, (new_entry['concept'],
              new_entry['entry'], new_entry['date'], new_entry['moodId']))

        id = db_cursor.lastrowid

        new_entry['id'] = id

        if new_entry['tags']:
            for tag in new_entry['tags']:
                db_cursor.execute("""
                INSERT INTO EntryTags
                    ( entry_id, tag_id )
                VALUES
                    ( ?, ? );
                """, (id, tag, ))
        
    return json.dumps(new_entry)

def update_entry(id, new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE journalentries
            SET
                concept = ?,
                entry = ?,
                date = ?,
                moodId = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'],
              new_entry['date'], new_entry['moodId'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True
