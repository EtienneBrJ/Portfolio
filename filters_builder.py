#!/usr/bin/python3
"""" Module regrouping all the side functions """
from datetime import datetime

def checkSeconds(seconds):
    """ Return a string depending on the value of sec (seconds)"""
    if seconds >= 3600:
        return "Il y a plus d'une heure"
    elif 3600 > seconds > 60:
        minute = int(seconds / 60)
        if minute == 1:
            return 'Il y a {} minute'.format(minute)
        return 'Il y a {} minutes'.format(minute)
    else:
        return 'Il y a {} secondes'.format(seconds)

def fromTimestampToNow(timestamp):
    """" Returns the number of seconds between the date (timestamp) and now """
    strDate = str(datetime.fromtimestamp(timestamp))
    blockDate=datetime.strptime(strDate, "%Y-%m-%d %H:%M:%S")
    return (datetime.now()-blockDate).seconds
