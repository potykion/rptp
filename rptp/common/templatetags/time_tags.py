import time
from django import template

register = template.Library()


@register.filter
def format_seconds(seconds):
    """
    Convert seconds to HH/MM/SS format.
    Args:
        seconds: Input seconds.

    Returns:
        Formatted string.

    >>> format_seconds(60)
    '00:01:00'
    """
    return time.strftime('%H:%M:%S', time.gmtime(seconds))
