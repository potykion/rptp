import time


def format_seconds(seconds):
    return time.strftime('%H:%M:%S', time.gmtime(seconds))


def truncate_left(str_, len_=50):
    splitted = str_.split()
    truncated = splitted.pop(0)
    for chunk in splitted:
        if len('{} {}'.format(truncated, chunk)) > len_:
            return truncated
        truncated += ' ' + chunk

    return truncated


def truncate_right(str_, len_=50):
    truncated = truncate_left(str_, len_)

    if truncated == str_:
        return ''

    return str_[len(truncated) + 1:]
