import datetime

import pytest

from api.utils import (calculate_date_since,
                       convert_date_to_ymd)


@pytest.fixture()
def fake_datetime_now(mocker):
    mock_dt = mocker.patch(
        'api.utils.datetime'
    )
    mock_dt.now.return_value = datetime.datetime(2023, 9, 14)
    yield mock_dt


@pytest.mark.parametrize(
    'param_expected',
    [
        (2, datetime.date(2023, 9, 12)),
        (3, datetime.date(2023, 9, 11)),
        (0, datetime.date(2023, 9, 14)),
    ]
)
def test_calculate_date_since(param_expected, fake_datetime_now):
    param, expected = param_expected
    res = calculate_date_since(param)
    assert res == expected


@pytest.mark.parametrize(
    'param_expected',
    [
        (datetime.datetime(2023, 9, 12), '2023-09-12'),
        (datetime.datetime(1985, 4, 11), '1985-04-11'),
    ]
)
def test_convert_date_to_ymd(param_expected):
    param, expected = param_expected
    res = convert_date_to_ymd(param)
    assert res == expected
