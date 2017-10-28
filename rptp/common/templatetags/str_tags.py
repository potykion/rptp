from django import template

register = template.Library()


@register.filter
def truncate_left(text: str, max_len=40):
    """
    Split input text, join its parts while result length is less than input length.

    Args:
        sep:
        text: Input text.
        max_len: Maximum length.

    Returns:
        Truncated text.

    >>> truncate_left('Ariel.temple Milf mature Ass Babes Няшка Русское домашние Порно anal fuck блондиночка сосёт Эротика Секс в попу Молоденькие br')
    'Ariel.temple Milf mature Ass Babes Няшка'
    >>> truncate_left('latinasextapes.17.09.25.alba.desilva.curvy.latina.futbol.babe')
    'latinasextapes.17.09.25.alba.desilva'
    """

    result = text

    for separator in [' ', '.', ',']:
        splitted = result.split(sep=separator)
        truncated = splitted.pop(0)

        for chunk in splitted:
            new_truncated = '{}{}{}'.format(truncated, separator, chunk)
            if len(new_truncated) > max_len:
                return truncated
            truncated = new_truncated

        if len(truncated) <= 50:
            return truncated

        result = truncated

    return result[:50]


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
