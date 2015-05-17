#!/usr/bin/env python

from flask import Flask, request, jsonify
app = Flask(__name__, static_url_path='')

# GET request this for the national data and stuff
# return json if possible

STATES = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']

@app.route('/nation')
def getNation():
    db = dict()
    for i in STATES:
        db[i] = '#ff0000'
    return jsonify(**db)

# GET request for when someone clicks on a state
# example: /state?s=va
@app.route('/state')
def getState():
    state = request.args.get('s')
    return False

@app.route('/')
def root():
    return app.send_static_file('index.html')

import sys

if __name__ == '__main__':
    # probably should use gunicorn or something
    app.run(host='0.0.0.0', port=int(sys.argv[1]))
