class Node:
    '''Node for use with doubly-linked list'''
    def __init__(self, item):
        self.item = item
        self.next = None
        self.prev = None

class OrderedList:
    '''A doubly-linked ordered list of items, from lowest (head of list) to highest (tail of list)'''

    def __init__(self):
        '''Use ONE dummy node as described in class
           ***No other attributes***
           DO NOT have an attribute to keep track of size'''
        self.head = Node(None)
        self.head.next = self.head
        self.head.prev = self.head
    def is_empty(self):
        '''Returns True if OrderedList is empty
            MUST have O(1) performance'''
        return self.head.next == self.head
    def add(self, item):
        '''Adds an item to OrderedList, in the proper location based on ordering of items
           from lowest (at head of list) to highest (at tail of list) and returns True.
           If the item is already in the list, do not add it again and return False.
           MUST have O(n) average-case performance.  Assume that all items added to your
           list can be compared using the < operator and can be compared for equality/inequality.
           Make no other assumptions about the items in your list'''
        if self.is_empty():
            n = Node(item)
            self.head.next = n
            self.head.prev = n
            n.next = self.head
            n.prev = self.head
            return True
        elif self.search(item):
            return False
        n = Node(item)
        currentNode = self.head.next
        while currentNode != self.head and item > currentNode.item:
            currentNode = currentNode.next
        n.next = currentNode
        n.prev = currentNode.prev
        currentNode.prev.next = n
        currentNode.prev = n
        return True
    def remove(self, item):
        '''Removes the first occurrence of an item from OrderedList. If item is removed (was in the list)
           returns True.  If item was not removed (was not in the list) returns False
           MUST have O(n) average-case performance'''
        currentNode = self.head.next
        while currentNode != self.head:
            if currentNode.item == item:
                currentNode.prev.next = currentNode.next
                currentNode.prev.next.prev = currentNode.prev
                return True
            else:
                currentNode = currentNode.next
        return False

    def index(self, item):
        '''Returns index of the first occurrence of an item in OrderedList (assuming head of list is index 0).
           If item is not in list, return None
           MUST have O(n) average-case performance'''
        node = self.head.next
        count = 0
        while node != self.head:
            if node.item == item:
                return count

            node = node.next
            count+=1



    def pop(self, index):
        '''Removes and returns item at index (assuming head of list is index 0).
           If index is negative or >= size of list, raises IndexError
           MUST have O(n) average-case performance'''
        if self.is_empty() or index < 0 or index >= self.size():
            raise IndexError
        count = 0
        currentNode = self.head.next
        while currentNode != self.head:
            if count == index:
                a = currentNode.item
                currentNode.prev.next = currentNode.next
                currentNode.prev.next.prev = currentNode.prev
                return a
            else:
                count+=1
                currentNode = currentNode.next


    def search(self, item):
        '''Searches OrderedList for item, returns True if item is in list, False otherwise"
           To practice recursion, this method must call a RECURSIVE method that
           will search the list
           MUST have O(n) average-case performance'''
        return self.search_helper(item, self.head.next)

    def search_helper(self, item, node):
        if node.item == item:
            return True
        if node.next != self.head:
            return self.search_helper(item, node.next)
        else:
            return False



    def python_list(self):
        '''Return a Python list representation of OrderedList, from head to tail
           For example, list with integers 1, 2, and 3 would return [1, 2, 3]
           MUST have O(n) performance'''
        lst = []
        node = self.head.next
        while node != self.head:
            lst.append(node.item)
            node = node.next
        return lst


    def python_list_reversed(self):
        '''Return a Python list representation of OrderedList, from tail to head, using recursion
           For example, list with integers 1, 2, and 3 would return [3, 2, 1]
           To practice recursion, this method must call a RECURSIVE method that
           will return a reversed list
           MUST have O(n) performance'''
        return self.python_list_reversed_helper(self.head.prev)

    def python_list_reversed_helper(self, node):
        if node == self.head:
            return []
        else:
            return [node.item] + self.python_list_reversed_helper(node.prev)

    def size(self):
        '''Returns number of items in the OrderedList
           To practice recursion, this method must call a RECURSIVE method that
           will count and return the number of items in the list
           MUST have O(n) performance'''
        return self.size_helper(self.head.next)
    def size_helper(self, node):
        if node == self.head:
            return 0
        return 1 + self.size_helper(node.next)