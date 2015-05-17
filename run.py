#!/usr/bin/env python

from flask import Flask
app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    return app.send_static_file('index.html')

import sys

if __name__ == '__main__':
    # probably should use gunicorn or something
    if len(sys.argv) >= 2:
        app.run(port=int(sys.argv[1]))
    else:
        app.run()
