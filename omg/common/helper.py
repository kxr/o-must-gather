import sys, os
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

from omg.common.config import Config

# This function is used to calculate age of the objects
# We compare the time reported in the yaml definition,
# with the timestamp of the yaml file (i.e, when it was generated).
# This should give us age of the object at the time of must-gather
# obj_time time is in standard format e.g: '2020-06-04T22:10:41Z'
# file_ts is unix ts e.g: 1590912494.0 (returned by os.path.getmtime)

def age(obj_time, file_ts):

    try:
        dt1 = parse(obj_time, ignoretz=True)
        dt2 = datetime.fromtimestamp(file_ts)
        rd = relativedelta(dt2, dt1)
    except:
        return 'Unknown'

    if rd.days > 0:
        return str(rd.days)+'d'
    elif rd.hours > 9:
        return str(rd.hours)+'h'
    elif rd.hours > 0 and rd.hours < 10:
        return str(rd.hours)+'h'+str(rd.minutes)+'m'
    elif rd.minutes > 9:
        return str(rd.minutes)
    elif rd.minutes > 0 and rd.minutes < 10:
        return str(rd.minutes)+'m'+str(rd.seconds)+'s'
    else:
        return str(rd.seconds)+'s'