def split_strip(str_, delimiter=','):
    return map(lambda login: login.strip(), str_.split(delimiter))


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