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
    session.post(url, data={'entry_type': 'text', 'skip_invalid_entries': True, 'entries': thing})
    out = decoder.decode(session.post('https://www.metamind.io/api/v1.2/classifiers/155/predict', data={"dataset_id": id}).content)
    # return {a[u'user_value']: (a[u'label'], a[u'probability']) for a in out[u'predictions']}
    hue = {}
    for o in out['predictions']:
        if o['label'] in hue:
            hue[o['label']] += 1
        else:
            hue[o['label']] = 1
    return hue


if __name__ == "__main__":
    # print sentiment()
    print sentiment((123, 456))
    print sentiment(['this is great', 'this also exists', 'this is shit', 'this is neutral', 'this also exists'])
    print sentiment(['this was a triumph', 'I\'m making a note here, HUGE SUCCESS', 'it\'s hard to overstate my satisfaction', 'aperture science', 'we do what we must, because we can', 'for the good of all of us except the ones who are dead', 'but there\'s no sense crying over every mistake', 'we\'ll just keep on trying till we run out of cake', 'and the science gets done', 'and you make a neat gun', 'for the people who are still alive', 'I\'m not even angry', 'I\'m being so sincere right now', 'even though you broke my heart and killed me', 'and tore me to pieces', 'and threw every piece into a fire', 'as they burned it hurt because I was so happy for you', 'but these points of data make a beautiful line', 'and we\'re out of beta we\'re releasing on time', 'so I\'m GLaD I got burned', 'think of all the things we learned', 'for the people who are still alive', 'go head and leave me', 'I think I\'d prefer to stay inside', 'maybe you\'ll find someone else to help you', 'maybe black mesa', 'that was a joke', 'HAH HAH', 'fat chance', 'anyways this cake is great it\'s so delicious and moist', 'look at me still talking while there\'s science to do',
                     'when I look out there it makes me GLaD I\'m not you', 'I\'ve experiments to run', 'there is research to be done', 'for the people who are still alive', 'and believe me I am still alive', 'I\'m doing science and I\'m still alive', 'I feel fantastic and I\'m still alive', 'and While you\'re dying I\'ll be still alive', 'and when you\'re dead I will be still alive', 'still alive', 'still alive'])
