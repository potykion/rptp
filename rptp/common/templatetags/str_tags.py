from django import template

register = template.Library()


@register.filter
def truncate_left(text, max_len=50):
    """
    Split input text, join its parts while result length is less than input length.

    Args:
        text: Input text.
        max_len: Maximum length.

    Returns:
        Truncated text.

    >>> truncate_left('Ariel.temple Milf mature Ass Babes Няшка Русское домашние Порно anal fuck блондиночка сосёт Эротика Секс в попу Молоденькие br')
    'Ariel.temple Milf mature Ass Babes Няшка Русское'
    """

    splitted = text.split()
    truncated = splitted.pop(0)
    for chunk in splitted:
        if len('{} {}'.format(truncated, chunk)) > max_len:
            return truncated
        truncated += ' ' + chunk

    return truncated


@register.filter
def truncate_right(text, max_len=50):
    """
    Truncate by left, shift input text by truncated text length.

    Args:
        text: Input text.
        max_len: Maximum length.

    Returns:
        Truncated text.

    >>> truncate_right('Ariel.temple Milf mature Ass Babes Няшка Русское домашние Порно anal fuck блондиночка сосёт Эротика Секс в попу Молоденькие br')
    'домашние Порно anal fuck блондиночка сосёт Эротика Секс в попу Молоденькие br'
    """
    truncated = truncate_left(text, max_len)

    if truncated == text:
        return ''

    return text[len(truncated) + 1:]
