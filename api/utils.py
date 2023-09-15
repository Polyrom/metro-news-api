from datetime import datetime, timedelta


def calculate_date_since_days(days: int) -> str:
    """
    Calculates date for the defined number of days ago
    :param days: number of days
    :return: date in format YYYY-mm-dd
    """
    return (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")


def normalize_date_for_response(date: str) -> str:
    """
    Formats date string dd.mm.YYYY into YYYY-mm-dd
    :param date: date string dd.mm.YYYY
    :return: date string YYYY-mm-dd
    """
    parsed_date = datetime.strptime(date, '%d.%m.%Y')
    return parsed_date.strftime('%Y-%m-%d')
