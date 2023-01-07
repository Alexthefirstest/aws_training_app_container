from functools import wraps

from source.file_logger import file_logger_v


def exceptions_handler(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseException as ex:
            file_logger_v.warning(str(ex))
            return {'exception occurred': str(ex)}

    return inner
