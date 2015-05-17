import simplejson
import requests
from random import randint

def sentiment(texts):
    thing = simplejson.dumps([{"label": None, "value": x} for x in texts])
    session = requests.Session()
    session.headers.clear()
    session.headers["Authentication"] = "Basic zzjfd812EiDqxeuqC91BnwaOk5YHWsh9FNUqkKnS8JFcwe8PHw"
    dataset = requests.post('https://www.metamind.io/api/v1.2/datasets', data={'name': 'temp' + randint(0, 10000000000).__str__(), 'private': False, 'data_type': 'text'})
    decoder = simplejson.JSONDecoder()
    id = decoder.decode(dataset.content)["id"]
    url = 'https://www.metamind.io/api/v1.2/datasets/' + id.__str__() + '/entries'
    print session.post(url, data={'entry_type': 'text', 'skip_invalid_entries': True, 'entries': thing}).content
    print session.get(url).content

sentiment(['abc', 'def', 'ghi'])
