import datetime as dt

from dateutil.relativedelta import relativedelta


def relativedelta_in_months(date1, date2):
    difference = relativedelta(
        dt.date.fromisoformat(date1), dt.date.fromisoformat(date2)
    )
    return difference.years * 12 + difference.months
