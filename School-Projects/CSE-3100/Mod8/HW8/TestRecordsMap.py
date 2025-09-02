# Import what you need
# Include unittests here. Focus on readability, including comments and docstrings.
from RecordsMap import LocalRecord, RecordsMap
import unittest

class TestLocalRecord(unittest.TestCase):
    def test_init(self):
        """Testing Initializer"""
        r1 = LocalRecord((41.8067, -72.2522))
        self.assertTrue(r1.pos==(41.8067, -72.2522))

    def test_hash(self):
        """Testing Hash function"""
        r1 = LocalRecord((41.8067, -72.2522))
        self.assertTrue(hash(r1) == 4272)

    def test_eq(self):
        """Testing eq function"""
        p1 = LocalRecord((41.8067, -72.2522))
        p2 = LocalRecord((41.8097, -72.1473))
        p3 = LocalRecord((41.3005, -72.4533))
        self.assertTrue(p1 == p2)
        self.assertFalse(p1 == p3)

    def test_add_report(self):
        """Testing add report function"""
        p1 = LocalRecord((41.8067, -72.2522))
        p1.add_report(15)
        self.assertTrue(p1.max == 15 and p1.min == 15)

class TestRecordsMap(unittest.TestCase):
    def test_add_one_report(self):
        '''Testing RecordsMap with one report'''
        m = RecordsMap()
        m.add_report((41.3005, -72.4533), 15)
        #testing len
        self.assertTrue(len(m) == 1)
        #testing getitem
        self.assertTrue(m[(41.3005, -72.4533)] == [15, 15])
        #testing contains
        self.assertTrue((41.3005, -72.4533) in m)

    def test_add_many_reports(self):
        '''Testing RecordsMap with multiple reports'''
        m = RecordsMap()
        m.add_report((41.3005, -72.4533), 15)
        m.add_report((40, -75), 20)
        m.add_report((40, -75), 15)
        m.add_report((45, -67), 15)
        m.add_report((45, -67), 25)
        #testing len
        self.assertTrue(len(m) == 3)
        #testing getitem
        self.assertTrue(m[(41.3005, -72.4533)] == [15, 15])
        self.assertTrue(m[(40, -75)] == [15, 20])
        self.assertTrue(m[(45, -67)] == [15, 25])
        #testing contains
        self.assertTrue((41.3005, -72.4533) in m)
        self.assertTrue((40, -75) in m)
        self.assertTrue((45, -67) in m)

    def test_rehash(self):
        '''Testing if the rehash method works'''
        m = RecordsMap(3)
        m.add_report((41.3005, -72.4533), 15)
        m.add_report((40, -75), 20)
        self.assertTrue(m.num_buckets() == 3)
        m.add_report((40, -75), 15)
        m.add_report((45, -67), 15)
        m.add_report((45, -67), 25)
        self.assertTrue(m.num_buckets() == 6)

# You need to add a line here to run the unittests
unittest.main()