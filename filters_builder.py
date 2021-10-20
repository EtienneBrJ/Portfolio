#!/usr/bin/python3
"""" Module regrouping all the side functions """
from datetime import datetime

def checkSeconds(seconds):
    """ Return a string depending on the value of sec (seconds)"""
    if seconds >= 3600:
        return "Plus d'1 heure"
    elif 3600 > seconds > 60:
        minute = int(seconds / 60)
        if minute == 1:
            return '{} minute ago'.format(minute)
        return '{} minutes ago'.format(minute)
    else:
        return 'Since {} sec'.format(seconds)

def fromTimestampToNow(timestamp):
    """" Returns the number of seconds between the date (timestamp) and now """
    strDate = str(datetime.fromtimestamp(timestamp))
    blockDate=datetime.strptime(strDate, "%Y-%m-%d %H:%M:%S")
    return (datetime.now()-blockDate).seconds
