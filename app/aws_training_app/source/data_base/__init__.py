from source.data_base.db_constants import TABLE_NAME
from source.data_base.images_worker import _execute_query_and_close_connection

CREATE_TABLE_SCRIPT = """CREATE TABLE IF NOT EXISTS `{0}` (
`name` VARCHAR(100) NOT NULL,
`size_bites` INT NOT NULL,
`file_extension` VARCHAR(45) NULL DEFAULT '',
`last_update_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (`name`),
UNIQUE INDEX `id_UNIQUE` (`name` ASC) VISIBLE);"""


def create_table():
    _execute_query_and_close_connection(CREATE_TABLE_SCRIPT.format(db_constants.TABLE_NAME))


create_table()
