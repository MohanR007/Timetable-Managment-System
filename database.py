import sqlite3
from flask import g

def connect_to_database():
    sql = sqlite3.connect("timetable.db")
    sql.row_factory = sqlite3.Row
    return sql

def get_database():
    if not hasattr(g, "timetable_db"):
        g.timetable_db = connect_to_database()
    return g.timetable_db

def close_database(e=None):
    db = g.pop("timetable_db", None)
    if db is not None:
        db.close()
