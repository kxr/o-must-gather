from datetime import datetime
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from loguru import logger as lg


def age(ts1, ts2, ts1_type="iso", ts2_type="epoch"):
    """Calculate age of the objects

    This function is used to calculate age of the objects
    We compare the time reported in the yaml definition,
    with the timestamp of the yaml file (i.e, when it was generated).
    This should give us age of the object at the time of must-gather
    By default, ts1 is considered in iso-8601 e.g: '2020-06-04T22:10:41Z'
    and ts2 is considered in unix/epoch format e.g: 1590912494.0 (returned by os.path.getmtime)


    Args:
        ts1 (str): First timestamp
        ts2 (str): Second timestamp
        ts1_type (str, optional): Type of fist timestamp. Defaults to "iso".
        ts2_type (str, optional): Type of second timestamp. Defaults to "epoch".

    Returns:
        str:    Human readable age e.g: 1d, 3m, 6h, 20s etc.
                Biggest unit is days (d) and smallest is (s)
    """
    try:
        if ts1_type == "iso":
            if isinstance(ts1, datetime):
                ts1 = ts1.isoformat()
            dt1 = parse(ts1, ignoretz=True)
        elif ts1_type == "epoch":
            dt1 = datetime.utcfromtimestamp(ts1)

        if ts2_type == "iso":
            if isinstance(ts2, datetime):
                ts2 = ts2.isoformat()
            dt2 = parse(ts2, ignoretz=True)
        elif ts2_type == "epoch":
            dt2 = datetime.utcfromtimestamp(ts2)

        rd = relativedelta(dt2, dt1)
    except Exception as e:
        lg.debug("error parsing timestamps: {}".format(e))
        return "Unknown"

    if rd.days > 0 or rd.months > 0 or rd.years > 0:
        days = int(rd.years * 365) + int(rd.months * 30) + int(rd.days)
        return str(days) + "d"
    elif rd.hours > 9:
        return str(rd.hours) + "h"
    elif rd.hours > 0 and rd.hours < 10:
        return str(rd.hours) + "h" + str(rd.minutes) + "m"
    elif rd.minutes > 9:
        return str(rd.minutes) + "m"
    elif rd.minutes > 0 and rd.minutes < 10:
        return str(rd.minutes) + "m" + str(rd.seconds) + "s"
    else:
        return str(rd.seconds) + "s"
