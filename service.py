from flask import Flask, request, render_template
import flask
import utils
import os
import logging
import sqlite3

service = Flask(__name__)

form = """<form method="POST">
    <input name="text">
    <input type="submit">
</form>"""

@service.route('/',methods=['GET','POST'])
def test():
    if request.method == "POST":
        text = request.form['text']
        processed_text = text.upper()
        return web_shorten(processed_text)
    else:
        return form

@service.errorhandler(400)
def no_url():
    return "URL not present or invalid",400

@service.errorhandler(409)
def already_used():
    return "shortcode already in use",409

@service.errorhandler(412)
def invalid_code():
    return "The provided shortcode is invalid",412

@service.errorhandler(404)
def not_found():
    return "Shortcode not found",404

@service.route('/shorten',methods=['POST'])
def shorten():

    shortcode = ""
    
    if request.method == 'POST':
        received = request.get_json(force = True)

        url = received["url"] if received["url"] else ""

        if len(url) < 2 or utils.check_url(url) == False:
            return no_url()

        conn = utils.create_connection("test.db")
        
        check = utils.check_entry(url, conn)
        db_url = check[1] if check else False
        
        if db_url and db_url == url:
            conn.close()
            return already_used()

        try:
            shortcode = received["shortcode"]
        except KeyError:
            logging.warn("No shortcode provided, generating one...")
            shortcode = utils.make_key(6)

        if utils.check_shortcode(shortcode) == False:
            conn.close()
            return invalid_code()

    _date = utils.get_date()
    utils.new_entry(url, shortcode, _date, _date, conn)
    conn.close()
    return flask.make_response(shortcode, 201)

@service.route('/web_shorten')
def web_shorten(url):

    url = url.strip()
    
    if len(url) < 2 or utils.check_url(url) == False:
        return no_url()

    conn = utils.create_connection("test.db")

    check = utils.check_entry(url, conn)
    
    db_url = check[1] if check else False

    if db_url and db_url == url:
        conn.close()
        return already_used()

    shortcode = utils.make_key(6)

    _date = utils.get_date()

    utils.new_entry(url, shortcode, _date, _date, conn)
    conn.close()

    return shortcode


@service.route('/<shortcode>')
def showShortcode(shortcode):
    """
    Receives a shortcode, check whether it's in the db and if so returns the corresponding url
    """
    try:
        conn = utils.create_connection("test.db")
        entry, url = utils.check_entry(shortcode, conn)
        if entry:
            newdate = utils.get_date()
            utils.update_entry(shortcode, conn)
            conn.close()
            resp = flask.make_response(url, 302)
            resp.headers["Location"] = url
            return resp
    except:
        conn.close()
        return not_found()

@service.route('/<shortcode>/stats')
def shortcodeStats(shortcode):
    """
    Receives a shortcode, check whether it's in the db and if so returns its stats in json
    """
 
    try:
        conn = utils.create_connection("test.db")
        entry, url = utils.check_entry(shortcode, conn)
        if entry:
            stats = utils.get_stats(shortcode, conn)
            stats = flask.jsonify(stats)
            conn.close()
            return flask.make_response(stats, 200)
    except:
        conn.close()
        return not_found()

if __name__ == '__main__':

    logging.basicConfig(level=logging.WARNING, filename="logs.log")
    
    if "test.db" in os.listdir():
        service.run(port=5000)
    else:
        logging.error("You need to create the test.db file first.\nRun python3 db.py")
