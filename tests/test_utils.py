import datetime

import pytest

from api.utils import (calculate_date_since_days,
                       normalize_date_for_response)


@pytest.fixture()
def fake_datetime_now(mocker):
    mock_dt = mocker.patch(
        'api.db_adapter.utils.datetime'
    )
    mock_dt.now.return_value = datetime.datetime(2023, 9, 14)
    yield mock_dt


@pytest.mark.parametrize(
    'param_expected',
    [
        (2, '2023-09-12'),
        (3, '2023-09-11'),
        (0, '2023-09-14'),
    ]
)
def test_calculate_date_since_days(param_expected, fake_datetime_now):
    param, expected = param_expected
    res = calculate_date_since_days(param)
    assert res == expected


@pytest.mark.parametrize(
    'param_expected',
    [
        ('12.09.2023', '2023-09-12'),
        ('11.04.1985', '1985-04-11'),
    ]
)
def test_normalize_date_for_response(param_expected):
    param, expected = param_expected
    res = normalize_date_for_response(param)
    assert res == expected
