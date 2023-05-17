from nepali_datetime import FiscalYear, datetime
import pytest

class TestFiscalYear:
    """Test Fiscal Year."""

    def test_now_before_aashar_masanta(self, monkeypatch):
        current_datetime = datetime(2080, 3, 1)
        monkeypatch.setattr('nepali_datetime.datetime', MockDatetime(current_datetime))
        assert FiscalYear.now() == "2079/2080"

    def test_now_after_aashar_masanta(self, monkeypatch):
        current_datetime = datetime(2080, 4, 1)
        monkeypatch.setattr('nepali_datetime.datetime', MockDatetime(current_datetime))
        assert FiscalYear.now() == "2080/2081"


# Helper class to mock the datetime.now() method
class MockDatetime:
    def __init__(self, datetime_obj):
        self.datetime_obj = datetime_obj

    def now(self):
        return self.datetime_obj