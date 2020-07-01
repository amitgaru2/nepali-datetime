import nepali_datetime


class TestInit:
    """Test attributes initialized when a instance of the class is created."""

    def test_max_date_gt_min_date(self):
        assert nepali_datetime.MAXYEAR > nepali_datetime.MINYEAR
