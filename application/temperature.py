import time 
import sqlite3 as lite 

#location of the data base
location = '../db.sqlite3'


def create_table(name):
    connection = lite.connect(location) 
    cursor = connection.cursor()
    sql_request = '''CREATE TABLE IF NOT EXISTS {table}
        (time TEXT, temperature REAL)'''.format('table': name)
    cursor.execute(sql_request)
    connection.commit()
