import pytest
from nepali_datetime import datetime
from unittest.mock import patch

@pytest.fixture
def mock_now():
    with patch.object(datetime, 'now') as mock:
        yield mock

def test_now_before_aashar_masanta(mock_now):
    mock_now.return_value = datetime(2080, 3, 1)
    fiscal_year = datetime.current_fiscal_year()
    assert fiscal_year == "2079/2080"

def test_now_after_aashar_masanta(mock_now):
    mock_now.return_value = datetime(2080, 4, 1)
    fiscal_year = datetime.current_fiscal_year()
    assert fiscal_year == "2080/2081"