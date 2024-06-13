import datetime
import math
from django import template
from django.utils import timezone as tz

register = template.Library()


@register.filter
def date_formatter(post_date):
    now = tz.now()

    return_str = ""

    time_passed = now - post_date

    days = time_passed.days

    if days > 0:
        # days more than 1 year
        if days >= 365:
            years = math.floor(days / 365)
            if years == 1:
                return f"1 year ago"
            else:
                return f"{years} years ago"

        # days more than a month
        if days >= 30:

            months = math.floor(days / 30)
            if months == 1:
                return f"1 month ago"
            else:
                return f"{months} months ago"

        # days more than a week
        if days >= 7:
            weeks = math.floor(days / 7)
            if weeks == 1:
                return f"1 week ago"
            else:
                return f"{weeks} weeks ago"

        # less than a week
        if days < 7:
            if days == 1:
                return f"{days} day ago"
            else:
                return f"{days} days ago"

    if days < 1:
        seconds = time_passed.seconds
        if seconds == 0:
            return "Just now"

        hours = math.floor(seconds/3600)
        if hours > 0:
            if hours == 1:
                return f"{hours} hour ago"
            else:
                return f"{hours} hours ago"

        minutes = math.floor(seconds/60)
        if minutes > 0:
            if minutes == 1:
                return f"{minutes} minute ago"
            else:
                return f"{minutes} minutes ago"

        return f"{seconds} seconds ago"
