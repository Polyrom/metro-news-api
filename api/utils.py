from datetime import datetime, timedelta, date


def calculate_date_since(days: int) -> date:
    """
    Calculates date for the defined number of days ago
    :param days: number of days
    :return: date object
    """
    return (datetime.now() - timedelta(days=days)).date()


def convert_date_to_ymd(date_to_format: datetime) -> str:
    """
    Converts datetime to YYYY-mm-dd format
    :param date_to_format: datetime object
    :return: formatted datetime string
    """
    return datetime.strftime(date_to_format, '%Y-%m-%d')
