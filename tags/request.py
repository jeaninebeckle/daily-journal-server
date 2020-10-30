import sqlite3
import json

from models.tag import Tag  

def get_all_tags():
    with sqlite3.connect("./dailyjournal.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.name
        FROM tags t
        """)

        tags = []

        dataset = db_cursor.fetchall()


        for row in dataset:

            tag = Tag(row['id'], row['name'])

            tags.append(tag.__dict__)

    return json.dumps(tags)

def get_single_tag(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.name
        FROM tags t
        WHERE t.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        tag = Tag(data['id'], data['name'])

        return json.dumps(tag.__dict__)
