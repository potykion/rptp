def split_strip(str_, delimiter=','):
    return map(lambda login: login.strip(), str_.split(delimiter))