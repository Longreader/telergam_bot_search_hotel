import datetime
from sqlite3 import Error
from loguru import logger

from loader import connection
from database.sql import execute_query, execute_read_query

from telebot import types
import typing


def set_sql(i_id: int,
            i_hotel_id: int,
            i_command: str,
            i_is_photo: int,
            i_nums_photo: int,
            i_nums_hotel: int,
            i_check_in: datetime.datetime,
            i_check_out: datetime.datetime) -> None:
    """
    SET parameters to SQL table
    :param i_id: User id
    :param i_hotel_id: Hotel id
    :param i_command:  User command
    :param i_is_photo: Bool photo attach
    :param i_nums_photo: Number of photo
    :param i_nums_hotel: Number of hotels
    :param i_check_in: Date of check in
    :param i_check_out: Date of check out
    :return: None
    """
    params = [i_id, i_hotel_id, i_command,
              i_is_photo, i_nums_photo, i_nums_hotel,
              i_check_in, i_check_out]
    create_users = """
    INSERT INTO
      hotels (id, hotel_id, command, is_photo, nums_photo,
      nums_hotel, check_in, check_out)
    VALUES
      (?, ?, ?, ?, ?, ?, ?, ?);
    """
    cursor = connection.cursor()
    try:
        cursor.execute(create_users, (params[0], params[1], params[2],
                                     params[3], params[4], params[5],
                                     params[6], params[7]))
        connection.commit()
        logger.debug("Query executed successfully")
    except Error as e:
        logger.exception(f"The error '{e}' occurred")


def get_sql(i_id: int) -> typing.Union[types.User, None]:
    """
    Request to DB to check if ID exist
    :param i_id: Users Chat id
    :return: User_ID or None
    """
    create_posts = """
    SELECT * FROM
      hotels
    WHERE 
      id=?;
    """
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(create_posts, (i_id,))
        result = cursor.fetchall()
        return result
    except Error as e:
        logger.exception(f"The error '{e}' occurred")

