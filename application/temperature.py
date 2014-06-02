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

def add_new_entry(table_name, data):
    connection = lite.connect(location) 
    cursor = connection.cursor()
    current_time = time.strftime("%H:%M:%S") #23:59:23
    sql_request = 'insert into {table} values (?,?)'.format('table':table_name)
    cursor.execute(sql_request, [current_time, data])
    connection.commit()


