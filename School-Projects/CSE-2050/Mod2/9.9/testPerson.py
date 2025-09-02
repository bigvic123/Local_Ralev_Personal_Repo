#1
import unittest
from Person import Person

#2
class TestPerson(unittest.TestCase):
    #3
    def test_init(self):
        obj = Person("John", "Smith")
        self.assertEqual(obj.fname, "John")
        self.assertEqual(obj.lname, "Smith")

    def test_print(self):
        obj = Person("John", "Smith")
        self.assertEqual(str(obj), "Student name: John Smith")

#4
unittest.main()
    
