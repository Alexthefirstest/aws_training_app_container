from contextlib import contextmanager

from mysql.connector import connect, Error

from source import custom_constants
from source.data_base import db_constants

_ADD_DATA_SCRIPT = "INSERT INTO `{table}` (`name`, `size_bites`, `file_extension`) VALUES ('{name}', '{size}', '{ext}');"

_DELETE_DATA_SCRIPT = "DELETE FROM `{table}` WHERE (`name` = '{name}');"

_ADD_OR_UPDATE_DATA_SCRIPT = """INSERT INTO `{table}` (`name`, `size_bites`, `file_extension`)
VALUES ('{name}', '{size}', '{ext}') ON DUPLICATE KEY UPDATE `size_bites`={size}, `file_extension`='{ext}';"""

_SELECT_DATA_SCRIPT_ALL = """SELECT `name`, `size_bites`, `file_extension`,
DATE_FORMAT(`last_update_date`, "%d/%m/%Y %H:%i:%s") FROM `{table}`ORDER BY `name` {limit};"""

_SELECT_DATA_SCRIPT_ONE = """SELECT `name`, `size_bites`, `file_extension`,
DATE_FORMAT(`last_update_date`, "%d/%m/%Y %H:%i:%s") FROM `{table}` WHERE `name` = '{name}';"""


@contextmanager
def _autocommit_connection_on_exit(commit=True):
    with connect(host=custom_constants.DB_HOST,
                 user=custom_constants.DB_USERNAME, password=custom_constants.DB_PASSWORD,
                 database=custom_constants.BASE_DATABASE_NAME) as connection:
        with connection.cursor() as cursor:
            yield cursor
        if commit:
            connection.commit()


def _execute_query_and_close_connection(script):
    with _autocommit_connection_on_exit() as cursor:
        cursor.execute(script)


def _execute_query_close_connection_and_fetch_result(script):
    with _autocommit_connection_on_exit(commit=False) as cursor:
        cursor.execute(script)
        return cursor.fetchall()


def delete_raw(name):
    _execute_query_and_close_connection(_DELETE_DATA_SCRIPT.format(table=db_constants.TABLE_NAME, name=name))


def add_or_update_image_metadata(name, size_in_bites, file_extension='', override=False):
    query_to_execute = _ADD_OR_UPDATE_DATA_SCRIPT if override else _ADD_DATA_SCRIPT
    try:
        _execute_query_and_close_connection(query_to_execute.format(table=db_constants.TABLE_NAME, name=name,
                                                                    size=size_in_bites, ext=file_extension))
    except Error as err:
        if 'Duplicate entry' in err.msg:
            raise Exception(r'image with this name already exist, choose "override" or rename it')


def get_one(name):
    fetched_data = _execute_query_close_connection_and_fetch_result(_SELECT_DATA_SCRIPT_ONE
                                                                    .format(table=db_constants.TABLE_NAME, name=name))
    return fetched_data[0] if fetched_data else None


def get_all(quantity=None, start_pos=None):
    limit = ''
    if quantity:
        limit = f'LIMIT {start_pos}, {quantity}' if start_pos else f'LIMIT {quantity}'

    fetched_data = _execute_query_close_connection_and_fetch_result(_SELECT_DATA_SCRIPT_ALL
                                                                    .format(table=db_constants.TABLE_NAME, limit=limit))
    return fetched_data
