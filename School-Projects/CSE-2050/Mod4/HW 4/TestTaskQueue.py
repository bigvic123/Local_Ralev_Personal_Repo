from TaskQueue import Task
from TaskQueue import TaskQueue
import unittest

class TestTask(unittest.TestCase):
    def test_init(self):
        '''checks if working'''
        a = Task(2, 4)
        self.assertEqual(a.id, 2)
        self.assertEqual(a.cycles_left, 4)
        
    def test_reduced_cycles(self):
        '''checks if working'''
        a = Task(2, 2)
        a.reduce_cycles(1)
        self.assertEqual(a.cycles_left, 1)

class TestQueue(unittest.TestCase):
    def test_init(self):
        '''checks if working'''
        a = Task(2, 4)
        b = TaskQueue(1)
        b.add_task(a)
        self.assertEqual(b.current, a)

    def test_add_task(self):
        '''checks if working'''
        a1 = Task(1, 2)
        a2 = Task(2, 2)
        a3 = Task(3, 2)
        b = TaskQueue(1)
        b.add_task(a1)
        b.add_task(a2)
        b.add_task(a3)

        self.assertEqual(b.current, a1)
        self.assertEqual(b.current.next, a2)
        self.assertEqual(b.current.prev, a3)
        self.assertEqual(b.current.next.next, a3)
        
    def test_remove_task(self):
        '''checks if working'''
        a1 = Task(1, 2)
        a2 = Task(2, 2)
        a3 = Task(3, 2)
        b = TaskQueue(1)
        b.add_task(a1)
        b.add_task(a2)
        b.add_task(a3)

        b.remove_task(2)
        self.assertEqual(b.current, a1)
        self.assertEqual(b.current.next, a3)
        self.assertEqual(b.current.prev, a3)
        
    def test_is_empty(self):
        '''checks if working'''
        a = TaskQueue(1)
        self.assertEqual(a.is_empty(), True)

    def test_execute_task(self):
        '''checks if working'''
        a1 = Task(1, 3)
        a2 = Task(2, 3)
        a3 = Task(3, 3)
        b = TaskQueue(1)
        b.add_task(a1)
        b.add_task(a2)
        b.add_task(a3)

        self.assertEqual(b.execute_tasks(), 9)

unittest.main()