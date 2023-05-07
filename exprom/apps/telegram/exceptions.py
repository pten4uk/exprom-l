class BotDBException(Exception):
    pass


class OnlyOneObjectError(BotDBException):
    """ Возможно существование только одного объекта данной модели """
