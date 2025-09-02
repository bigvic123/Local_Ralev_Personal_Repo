from LinkedList import LinkedList

class Stack_L:
    def __init__(self):
        self._L = list()        # Composition: the Stack_L class has a List
    #Creating push and pop method for stack of list
    def push(self, item):
        self._L.append(item)

    def pop(self):
        return self._L.pop()


class Stack_LL:
    def __init__(self):
        self._LL = LinkedList() # Composition: the Stack_LL class has a Linked List
    #creating push and pop method for stack of linked list
    def push(self, item):
        self._LL.add_first(item)

    def pop(self):
        return self._LL.remove_first()


class Queue_L:
    def __init__(self):
        self._L = list()

    #creating enqueue and dequeue methods for list
    def enqueue(self, item):
        self._L.append(item)

    def dequeue(self):
        return self._L.pop(0)

class Queue_LL:
    def __init__(self):
        self._LL = LinkedList()

    #creating enqueue and dequeue methods for linked list
    def enqueue(self, item):
        self._LL.add_first(item)

    def dequeue(self):
        return self._LL.remove_last()



if __name__ == '__main__':
    
    #Creating List and Linked list for testing
    ##########Test Stack_L##########
    list1 = Stack_L()
    list1.push(4)
    list1.push(5)
    list1.push(6)
    assert list1.pop() == 6

    ##########Test Stack_LL#########
    
    linkedlist1 = Stack_LL()
    linkedlist1.push(1)
    linkedlist1.push(2)
    linkedlist1.push(3)
    assert linkedlist1.pop() == 3

    ##########Test Queue_L##########
    list2 = Queue_L()
    list2.enqueue(4)
    list2.enqueue(6)
    list2.enqueue(8)
    assert list2.dequeue() == 4

    ##########Test Queue_LL#########
    linkedlist2 = Queue_LL()
    linkedlist2.enqueue(1)
    linkedlist2.enqueue(3)
    linkedlist2.enqueue(5)
    assert linkedlist2.dequeue() == 1
