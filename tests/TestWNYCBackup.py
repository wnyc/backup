from datetime import datetime, date, timedelta
from wnyc_backup import count_right_zero_bits, kill_date
from unittest2 import TestCase

class TestBitCount(TestCase):
    expected_bit_counts = {1:0, 2:1, 3:0, 4:2, 5:0, 6:1, 7:0, 8:3, 9:0, 10:1}

    @staticmethod
    def reference_zero_bits(i):
        return (("".join(list(reversed(list(bin(i)))))).find('1'))

    def test_reference(self):
        "Confirm the refernece duration generates correct values"
        for i, expected in self.expected_bit_counts.items():
            self.assertEquals(self.reference_zero_bits(i), expected)

    def test_count_right_zero_bits(self):
        for x in range(1, 10000):
            self.assertEquals(self.reference_zero_bits(x), count_right_zero_bits(x))
            

class KillDateTest():

    def test_does_not_crash(self):
        kill_date(self.d)

    def test_is_in_future(self):
        self.assertGreater(kill_date(self.d), self.expected_date)

class TestKillDate(TestCase):
    @staticmethod
    def is_power_of_two(v):
        """Adaptation from CACM 3 (1960), 322"""
        return (v & (v-1)) == 0

    def test_difference_is_always_power_of_two(self):
        now = date(2013,1,1)
        for _ in range(10000):
            self.assertTrue(self.is_power_of_two(kill_date(now).toordinal() - now.toordinal()))
            now += timedelta(days=1)
    
class TestKillDateWithDatetime(KillDateTest, TestCase):
    d = datetime.now()
    expected_date = d.date()

class TestKillDateWithDate(KillDateTest, TestCase):
    d = date.today()
    expected_date = d

class TestKillDatewithOrdinal(KillDateTest, TestCase):
    d = datetime.now().toordinal()
    expected_date = date.fromordinal(d)
