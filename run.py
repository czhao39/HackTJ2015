#!/usr/bin/env python

from flask import Flask, request, jsonify
import os
import urlparse
import psycopg2

import urlparse
import psycopg2

app = Flask(__name__, static_url_path='')
app.config['DEBUG'] = True

# GET request this for the national data and stuff
# return json if possible

STATES = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

def getConnection():
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    return psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)

@app.route('/testdb')
def testDatabase():
    try:
        conn = getConnection()
        if conn != None:
            conn.close()
            return "<pre>Database connected successfully!</pre>"
        return "<pre>Failed to connect to database!</pre>"
    except Exception as e:
        return "<pre>" + str(e) + "</pre>"

from random import random

@app.route('/nation')
def getNation():
    p = request.args.get('p')
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT state, pos, neg FROM tweets WHERE candidate = %s", [p])
    rs = cursor.fetchall()
    conn.close()
    db = dict()
    for i in rs:
        db[i[0]] = [i[1], i[2]]
    for j in STATES:
        if not j in db:
            db[j] = [0, 0]
    assert len(db) >= 50
    return jsonify(**db)

# GET request for when someone clicks on a state
# example: /state?s=va
@app.route('/state')
def getState():
    state = request.args.get('s')
    tmp = dict()
    tmp['state'] = state
    return jsonify(tmp)

@app.route('/')
def root():
    return app.send_static_file('index.html')


import sys

if __name__ == '__main__':
    # probably should use gunicorn or something
    app.run(host='0.0.0.0', port=int(sys.argv[1]))
