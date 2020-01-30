import sqlite3
from sqlite3 import Error
import os

#####################################################
## THIS SCRIPT CREATES THE test.db SQLITE DATABASE ##
#####################################################

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    finally:
        if conn:
            print("connected!", conn)
            return conn



def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print("Table created!")
    except Error as e:
        print(e)

if __name__ == '__main__':
    if "test.db" not in os.listdir():
        newtable = """ CREATE TABLE IF NOT EXISTS visitors (
        url TEXT,
        shortcode TEXT,
        lastRedirect TEXT,
        redirectCount INTEGER,
        created TEXT
        ); """

        conn = create_connection("test.db")
        create_table(conn, newtable)