import datetime


def daterange(date_from, date_to, step=None):
    if step is None:
        step = datetime.timedelta(days=1)

    current_date = date_from
    while current_date < date_to:
        yield current_date
        current_date += step
