from typing import Any
from collections.abc import MutableSequence


class LinkedListNode:
    def __init__(self, data: Any, links_to: 'LinkedListNode' = None):
        self.data = data
        self.next = links_to


class LinkedList(MutableSequence):
    def __init__(self, start: LinkedListNode = None):
        if not isinstance(start, LinkedListNode):
            raise TypeError
        self.start = start

    def __len__(self) -> int:
        if not self.start:
            return 0
        length = 1
        next_node = self.start.next
        while next_node is not None:
            if next_node == self.start:
                raise AttributeError("Cycle found!")
            length += 1
            next_node = next_node.next
        return length

    def __getitem__(self, item: int) -> LinkedListNode:
        if self.__len__() - 1 < item:
            raise IndexError
        if item == 0:
            return self.start
        next_node = self.start.next
        if item == 1:
            return next_node
        for _ in range(item - 1):
            next_node = next_node.next
        return next_node
