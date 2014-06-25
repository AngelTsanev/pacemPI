import time 
import sqlite3 as lite
from tmp102 import tmp102_read_temperature 

#location of the data base
location = '../db.sqlite3'
CURRENT_DAY_TABLE = 'current_day'
LAST_WEEK_TABLE = 'last_week'
HISTORY_TABLE_NAME = 'history'
#so we assume we have created these two tables manualy

'''
To create tables enter the SQLite shell:

$ sqlite3 db.sqlite3 

In the SQLite shell enter these commands to create a table called last_week:

   BEGIN; 
   CREATE TABLE current_day (timestamp DATETIME, temperature NUMERIC);
   CREATE TABLE last_week (timestamp DATETIME, temperature NUMERIC);
   CREATE TABLE history (timestamp DATETIME, temperature NUMERIC); 
   COMMIT;

'''

def add_new_entry(temperature):
    #current_time = time.strftime("%H:%M:%S") #23:59:23
    connection = lite.connect(location) 
    cursor = connection.cursor()
    #sql_request = 'insert into {table} values (?,?)'.format('table':CURRENT_DAY_TABLE)
    #cursor.execute(sql_request, [current_time, data])
    cursor.execute("INSERT INTO {} values(datetime('now'), (?))"
                  .format(CURRENT_DAY_TABLE), (temperature,))

    connection.commit()
    cursor.close()
    connection.close()


def mesure_temperature():
    while True:
        time.sleep(5) 
        #date = time.strftime("%d/%m/%Y") #00/00/0000
        temperature = tmp102_read_temperature()
        #create_table(date)
        add_new_entry(temperature)
        print(temperature)

mesure_temperature()
