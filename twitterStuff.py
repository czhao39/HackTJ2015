import twitter
from twitterHelper import *
import simplejson
import run
import time
import metaMinds

def fillDb(cursor):
    jsonStr = open("static/data/keywords.json").read()
    jsonDict = simplejson.JSONDecoder().decode(jsonStr)
    statesJsonStr = open("static/data/states.json").read()
    statesJsonDict = simplejson.JSONDecoder().decode(statesJsonStr)
    mainDict = {}
    apiJsonStr = open("static/data/keys.json").read()
    apiJsonDict = simplejson.JSONDecoder().decode(apiJsonStr)
    for candidate in jsonDict.items():
        mainDict[candidate[0]] = {}
    api = twitter.Api(consumer_key=apiJsonDict[0]["API_KEY"], consumer_secret=apiJsonDict[0]["API_SECRET"], access_token_key=apiJsonDict[0]["ACCESS_TOKEN"], access_token_secret=apiJsonDict[0]["ACCESS_TOKEN_SECRET"])
    apiIndex = 0
    for candidate in mainDict.keys():
        print "doing candidate " + candidate
        for state in statesJsonDict.items():
            print "doing state " + state[0]
            statuses = []
            for term in jsonDict[candidate]:
                while True:
                    try:
                        api = twitter.Api(consumer_key=apiJsonDict[apiIndex]["API_KEY"], consumer_secret=apiJsonDict[apiIndex]["API_SECRET"], access_token_key=apiJsonDict[apiIndex]["ACCESS_TOKEN"], access_token_secret=apiJsonDict[apiIndex]["ACCESS_TOKEN_SECRET"])
                        statuses.extend(getSearch(twit=api, query=term + " place:"+state[1], count=100))
                    except IndexError:
                        pass
                    except twitter.error.TwitterError:
                        print "rate limit exceeded"
                        if (apiIndex > 14):
                            apiIndex = 0
                            print "switch to api key 0"
                            time.sleep(60)
                            print "checking for rate limit deexceedtion"
                        else:
                            apiIndex += 1
                            print "switch to api key " + apiIndex.__str__()
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
            try:
                cursor.execute("INSERT INTO tweets (candidate, state, pos, neg) VALUES (%(str)s, %(str)s, %(int)s, %(int)s", (candidate[0], state[0], metaMinds.sentiment(state[1])[u'positive'], metaMinds.sentiment(state[1])[u'negative']))
            except Exception:
                pass

cursor = run.getConnection().cursor()
fillDb(cursor)