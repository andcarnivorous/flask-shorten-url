from flask import Flask
from flask import request
import flask
import utils
import os
import logging

service = Flask(__name__)

@service.route('/')
def test():
    return 'Test app for job application'

@service.errorhandler(400)
def no_url():
    return "URL not present",400

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

        if len(url) < 2:
            return no_url()

        check = utils.check_entry(url)
        db_url = check[1] if check else False
        
        if db_url and db_url == url:
              return already_used()

        try:
            shortcode = received["shortcode"]
        except:
            logging.warn("No shortcode provided, generating one...")
            shortcode = utils.make_key(6)

        if utils.check_shortcode(shortcode) == False:
            return invalid_code()

    _date = utils.get_date()
    utils.new_entry(url, shortcode, _date, _date)
    return flask.make_response(shortcode, 201)

@service.route('/<shortcode>')
def showShortcode(shortcode):
    """
    Receives a shortcode, check whether it's in the db and if so returns the corresponding url
    """
    try:
        entry, url = utils.check_entry(shortcode)
        if entry:
            newdate = utils.get_date()
            utils.update_entry(shortcode)
            resp = flask.make_response(url, 302)
            resp.headers["Location"] = url
            return resp
    except:
        return not_found()

@service.route('/<shortcode>/stats')
def shortcodeStats(shortcode):
    """
    Receives a shortcode, check whether it's in the db and if so returns its stats in json
    """
 
    try:
        entry, url = utils.check_entry(shortcode)
        if entry:
            stats = utils.get_stats(shortcode)
            stats = flask.jsonify(stats)
            return flask.make_response(stats, 200)
    except:
        return not_found()

if __name__ == '__main__':

    logging.basicConfig(level=logging.WARNING, filename="logs.log")
    
    if "test.db" in os.listdir():
        service.run(host="0.0.0.0")
    else:
        logging.error("You need to create the test.db file first.\nRun python3 db.py")
