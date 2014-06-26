import sqlite3 as lite

conn = lite.connect('../db.sqlite3')
cur = conn.cursor()

def get_posts():
    cur.execute("SELECT * FROM current_day")
    conn.commit()
    print(cur.fetchall())

get_posts()
