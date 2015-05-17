import twitter
from twitterHelper import *
import simplejson
import run
import time
import metaMinds

def fillDb(cursor, api):
    jsonStr = open("static/data/keywords.json").read()
    jsonDict = simplejson.JSONDecoder().decode(jsonStr)
    statesJsonStr = open("static/data/states.json").read()
    statesJsonDict = simplejson.JSONDecoder().decode(statesJsonStr)
    mainDict = {}
    for candidate in jsonDict.items():
        mainDict[candidate[0]] = {}
    for candidate in mainDict.keys():
        print "doing candidate " + candidate
        for state in statesJsonDict.items():
            print "doing state " + state[0]
            statuses = []
            for term in jsonDict[candidate]:
                while True:
                    try:
                        statuses.extend(getSearch(twit=api, query=term + " place:"+state[1], count=100))
                    except IndexError:
                        pass
                    except twitter.error.TwitterError:
                        print "rate limit exceeded"
                        time.sleep(60)
                        print "checking for rate limit deexceedtion"
                        continue
                    break
            tweets = []
            for status in statuses:
                tweets.append(status._text)
            mainDict[candidate][state[0]] = tweets

    print mainDict
    f = open("antistupidity.json", "w")
    f.write(simplejson.dumps(mainDict))
    f.close()

    for candidate in mainDict.items():
        for state in candidate[1].items():
            cursor.execute("INSERT INTO tweets (candidate, state, pos, neg) VALUES (%(str)s, %(str)s, %(int)s, %(int)s", (candidate[0], state[0], metaMinds.sentiment(state[1])[u'positive'], metaMinds.sentiment(state[1])[u'negative']))

api = twitter.Api(consumer_key="kVPvvr7To3gmFhi1hqHiOMTOk", consumer_secret="ThxenYosQipFLuievc4rZcFcFzDu5b2xe5utOParzhh4YJoHgh", access_token_key="2924997039-Cygnh0IdQ2p1A8tLy9ulzLo4ShZf9slswefWPhD", access_token_secret="wcfN2N90oUVjmVEXfdIx4FeImO2A1GEWwv63GOg4w0Ccl")
cursor = run.getConnection().cursor()
fillDb(cursor, api)