from flask import jsonify
def sentiment(texts):
    text = [{"label": None, "value": x} for x in texts]
