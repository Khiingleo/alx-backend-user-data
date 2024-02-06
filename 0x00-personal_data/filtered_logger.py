#!/usr/bin/env python3
"""
contains filtered data
"""
import re
from typing import List
import logging
from os import getenv
import mysql.connector


PII_FIELDS = ('name', 'email', 'password', 'ssn', 'phone')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initialization"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter incoming log records"""
        msg = logging.Formatter(self.FORMAT).format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, seperator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(field + "=.*?" + seperator,
                         field + "=" + redaction + seperator, message)
    return message


def get_logger() -> logging.Logger:
    """returns a logging.Logger obj"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to a mysql database"""
    db = mysql.connector.connection.MySQLConnection(
        user=getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=getenv('PERSONAL_DATA_DB_NAME')
    )
    return db


def main() -> None:
    """main function"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    fields = []
    result = []
    for field in cursor.description:
        fields.append(field[0] + "=")

    logger = get_logger()

    for row in cursor:
        for i in range(len(fields)):
            result.append(fields[i] + str(row[i]) + ";")
        logger.info(" ".join(result))

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
