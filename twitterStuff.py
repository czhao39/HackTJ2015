import twitter
from greysFancyTwitterGarbage import *
import requests

import simplejson

api = twitter.Api(consumer_key="kVPvvr7To3gmFhi1hqHiOMTOk", consumer_secret="ThxenYosQipFLuievc4rZcFcFzDu5b2xe5utOParzhh4YJoHgh", access_token_key="2924997039-Cygnh0IdQ2p1A8tLy9ulzLo4ShZf9slswefWPhD", access_token_secret="wcfN2N90oUVjmVEXfdIx4FeImO2A1GEWwv63GOg4w0Ccl")

r = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params={"latlng": "", "key": "AIzaSyCPk9E5t02n-hQHfRqOLZFGFAcYbPCtTVk"})
jsonString = open("static/data/keywords.txt").read()
jsonDict = simplejson.JSONDecoder().decode(jsonString)
masterDict = {}
for tuple in jsonDict.items():
    statuses = []
    for term in tuple[1]:
        #todo: play around with resType
        statuses.extend(getSearch(twit=api, query=term, count=100))
    tweets = []
    for status in statuses:
        tweets.append(status._text)
    masterDict[tuple[0]] = tweets