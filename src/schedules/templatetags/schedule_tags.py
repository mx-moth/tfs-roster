import datetime
from django import template

register = template.Library()


def css(styles):
    return '; '.join('{0}:{1}'.format(*v) for v in styles.iteritems())


def seconds(time):
    return time.hour * 60 * 60 + time.minute * 60 + time.second


@register.filter
def by_days(schedule, dates):
    days_dict = {date: None for date in dates}
    days_dict.update({a.date: a for a in schedule.filter(date__in=(dates))})
    return [(date, days_dict.get(date, None)) for date in dates]


seconds_in_a_day = datetime.timedelta(days=1).total_seconds()


@register.filter
def position(availability):
    start = seconds(availability.start)
    end = seconds(availability.end)

    diff = (end - start) % seconds_in_a_day
    if diff == 0:
        diff = seconds_in_a_day

    left = "{:.6%}".format(start / seconds_in_a_day)
    width = "{:.6%}".format(diff / seconds_in_a_day)

    return css({
        'left': left,
        'width': width,
    })
