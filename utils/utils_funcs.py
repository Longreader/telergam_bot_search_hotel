import datetime


def separate(date: datetime.datetime.time or str) -> list:
    """
    Function separate date by day, month, year
    and return list
    :param date: Datetime date
    :return: List contains day, month, year
    """
    if type(date) == str:
        tmp = date.split('-')
        return [int(tmp[1]), int(tmp[2]), int(tmp[0])]
    else:
        tmp = date.strftime('%m %d %y').split()
        return [int(item) for item in tmp]
