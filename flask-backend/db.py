import sqlite3

conn = sqlite3.connect("posts.sqlite")

cursor = conn.cursor()
sql_query = """ CREATE TABLE book (
    displayName TEXT NOT NULL,
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    images TEXT NOT NULL,
    texts TEXT NOT NULL,
    username TEXT NOT NULL,
    verified BIT
)"""
cursor.execute(sql_query)

