import transliterate


def slugify(russian_text: str):
    """ Переделывает русский текст в английский вида: angliski-text """

    return transliterate.slugify(russian_text)

