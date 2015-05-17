import twitter
from twitterHelper import *
import simplejson
import run

def fillDb(cursor, api):
    jsonStr = open("static/data/keywords.json").read()
    jsonDict = simplejson.JSONDecoder().decode(jsonStr)
    statesJsonStr = open("static/data/states.json").read()
    statesJsonDict = simplejson.JSONDecoder().decode(statesJsonStr)
    mainDict = {}
    for candidate in jsonDict.items():
        mainDict[candidate[0]] = {}
    for candidate in mainDict.items():
        for state in statesJsonDict.items():
            statuses = []
            for term in jsonDict[candidate[0]]:
                statuses.extend(getSearch(twit=api, query=term + " place:"+state[1], count=100))
            tweets = []
            for status in statuses:
                tweets.append(status._text)
            candidate[state[0]] = tweets

    print mainDict

    for candidate in mainDict.items():
        for state in candidate[1].items():
            cursor.execute("INSERT INTO tweets (candidate, state, pos, neg, color) VALUES (%(str)s, %(str)s, %(int)s, %(int)s", {candidate[0], state[0],      })

api = twitter.Api(consumer_key="kVPvvr7To3gmFhi1hqHiOMTOk", consumer_secret="ThxenYosQipFLuievc4rZcFcFzDu5b2xe5utOParzhh4YJoHgh", access_token_key="2924997039-Cygnh0IdQ2p1A8tLy9ulzLo4ShZf9slswefWPhD", access_token_secret="wcfN2N90oUVjmVEXfdIx4FeImO2A1GEWwv63GOg4w0Ccl")
cursor = run.getConnection().cursor()
fillDb(cursor, api)