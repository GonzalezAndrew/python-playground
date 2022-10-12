"""
Implementing a linked list in Python.
"""


class Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_head(self, data):
        new_node = Node(data, self.head)
        self.head = new_node

    def insert_at_tail(self, data):
        if self.head is None:
            self.head = Node(data)
            return

        current = self.head
        while current.next:
            current = current.next

        current.next = Node(data)

    def insert_values(self, data_list):
        self.head = None
        for data in data_list:
            self.insert_at_tail(data)

    def get_length(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def remove_at_index(self, index):
        if index < 0 or index >= self.get_length():
            print("Index out of bounds")
            return

        # remove head if index is 0
        if index == 0:
            self.head = self.head.next
            return

        # create iterator obj
        current = self.head

        for _ in range(index - 1):
            current = current.next

        current.next = current.next.next

    def insert_at_index(self, index, data):
        if index < 0 or index > self.get_length():
            print("Index out of bounds")
            return

        if index == 0:
            self.insert_at_head(data)
            return

        current = self.head
        for _ in range(index - 1):
            current = current.next

        new_node = Node(data, current.next)
        current.next = new_node

    def print(self):
        if self.head is None:
            print("Empty list")
            return
        else:
            current = self.head
            while current:
                print(current.data, end="-->")
                current = current.next


if __name__ == "__main__":
    ll = LinkedList()
    ll.insert_values([1, 2, 3, 4, 5])

    ll.print()
    print("")
    ll.remove_at_index(2)
    ll.print()
    print("")
    ll.insert_at_index(2, 6)
    ll.print()
