import sqlite3
import typing
from sqlite3 import Error
from loguru import logger


def create_connection(path: str) -> sqlite3.Connection:
    """
    Create connection to DataBase
    :param path: Path to DB dir
    :return: Connection object
    """
    connection = None
    try:
        connection = sqlite3.connect(path, check_same_thread=False)

        logger.debug("Connection to SQLite DB successful")
    except Error as e:
        logger.exception(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query) -> None:
    """
    Execute command
    :param connection: Connection object
    :param query: Command to execute
    :return:
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        logger.debug("Query executed successfully")
    except Error as e:
        logger.exception(f"The error '{e}' occurred")


def execute_read_query(connection: sqlite3.Connection, query: typing.Any):
    """
    Execute command to read
    :param connection: Connection object
    :param query: Command to execute
    :return:
    """
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        logger.debug(f"The error '{e}' occurred")


def create_request_table(connection: sqlite3.Connection) -> None:
    """
    Create Users table
    :param connection: Connection object
    :return: None
    """
    create_posts = """
    CREATE TABLE IF NOT EXISTS hotels(
      id INTEGER, 
      hotel_id INT,
      command TEXT,
      is_photo INT,
      nums_photo INT,
      nums_hotel INT,
      check_in DATE,
      check_out DATE
    );
    """
    execute_query(connection, create_posts)
