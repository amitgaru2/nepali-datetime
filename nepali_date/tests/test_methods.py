from nepali_date.date import NepaliDate


class TestMethods:
    """Test helper methods of NepaliDate."""

    def test_strfdate(self):
        nep_date = NepaliDate(2051, 10, 1)
        assert nep_date.strfdate('%y %m %d %a') == '51 10 01 Sun'
        assert nep_date.strfdate('%Y %A') == '2051 Sunday'
        assert nep_date.strfdate('%b %B') == 'Mag Magh'

    def test_strpdate(self):
        nep_date = NepaliDate.strpdate(' 2051/10/01', fmt=' %Y/%m/%d')
        assert nep_date == NepaliDate(2051, 10, 1)
