import string
import datetime
import random
import sqlite3
from sqlite3 import Error
from db import create_connection

def make_key(_range: int) -> string:
    """
    Creates a random shortcode made up by alphanumeric characters and underscore
    :param _range: length of shortcode
    :return: alphanumeric shortcode
    """
    alphanum = string.digits + string.ascii_letters + "_"
    key = ""
    for x in range(_range):
        key += random.choice(alphanum)

    return key

def check_shortcode(shortcode: str) -> bool:
    """
    Check whether a shortcode is only alphanumeric and 6 characters long.
    :param shortcode: shortcode to check
    :return: True if the shortcode is ok
    """
    
    standard = string.digits+string.ascii_letters+"_"
    
    if len(shortcode) != 6:
        return False
    
    for x in shortcode:
        if x not in standard:
            return False

    return True

def get_date():
    return datetime.datetime.now().isoformat()

def new_entry(url, shortcode, lastRedirect, created):
    """
    Adds a new entry to the database
    :param url: url to add into the database
    :param shortcode: 6 character long alphanumeric shortcode
    :param lastRedirect: last time someone used the redirect
    :param created: when the shortcode was created
    """
    sql = """INSERT INTO visitors (url, shortcode, lastRedirect, redirectCount, created)
    VALUES ('%s', '%s', '%s', 1, '%s')""" % (url, shortcode, lastRedirect, created)
    conn = create_connection("test.db")
    if conn:
        c = conn.cursor()
        try:
            c.execute(sql)
        except sqlite3.Error as error:
            return Error
        conn.commit()
        conn.close()
        
def check_entry(entry):
    """
    Check whether a url or shortcode is already present in the db.
    :param entry: url or shortcode
    :return: False if not present, url and shortcode if already present
    """
    conn = create_connection("test.db")
    if conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM visitors")
        rows = c.fetchall()
        conn.close()
        for row in rows:
            if row["shortcode"] == str(entry) or row["url"] == str(entry):
                return (row["shortcode"], row["url"])
        return False

def update_entry(shortcode):
    """
    Updates lastRedirect and redirectCount when someone uses the shortcode
    :param shortcode: shortcode used
    """
    conn = create_connection("test.db")
    if conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM visitors")
        rows = c.fetchall()
        match = [i for i in rows if i["shortcode"] == shortcode][0]
        match = match["shortcode"]
        assert isinstance(match, str)
        newdate = get_date()
        sql = """UPDATE visitors SET lastRedirect = '%s', redirectCount = redirectCount + 1 
        WHERE shortcode = '%s'""" % (newdate, match)

        c.execute(sql)
        conn.commit()
        conn.close()

def get_stats(shortcode):
    """
    Returns redirectCount, created and lastRedirect date from a shortcode
    :param shortcode: shortcode from which to pull stats
    :return: dictionary with redirectCount, created and lastRedirect
    """
    conn = create_connection("test.db")
    if conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM visitors")
        rows = c.fetchall()
        conn.close()
        match = [i for i in rows if i["shortcode"] == shortcode]
        if len(match) != 1:
            return False
        match = match[0]
        features = ["created","lastRedirect","redirectCount"]
        stats = {str(i):0 for i in features}
        for i in features:
            stats[i] = match[i]

        return stats
