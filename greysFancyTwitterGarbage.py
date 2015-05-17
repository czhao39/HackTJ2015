def getUserTimeline(twit, handle, count):
    """
    :type count: int
    :type handle: str
    :type twit: twitter.Api
    :return: list
    """
    out = []
    lastMax = None
    while count > 0:
        if lastMax is not None:
            out.extend(twit.GetUserTimeline(screen_name=handle, count=200 if count > 200 else count, max_id=lastMax - 1))
        else:
            out.extend(twit.GetUserTimeline(screen_name=handle, count=200 if count > 200 else count))
        lastMax = out[-1].id
        count -= 200
    return out


def getSearch(twit, query, count, resType='mixed'):
    """
    :type twit: twitter.Api
    :type query: str
    :type count: int
    :type resType: str
    """
    out = []
    lastMax = None
    while count > 0:
        if lastMax is not None:
            out.extend(twit.GetSearch(term=query, count=100 if count > 100 else count, max_id=lastMax - 1, result_type=resType))
        else:
            out.extend(twit.GetSearch(term=query, count=100 if count > 100 else count, result_type=resType))
        lastMax = out[-1].id
        count -= 100
    return out