from typing import Any, Iterable
from collections.abc import Sequence, MutableSequence


class ImmutableChain(Sequence):
    class Node:
        def __init__(self, data: Any, links_to: 'ImmutableChain.Node' = None):
            self.data = data
            self.next = links_to

    def __init__(self):
        self._start = None
        self._length = 0
        self._last_node = None

    def __repr__(self) -> str:
        s = '['
        next_node = self._start
        for _ in range(self._length):
            s += repr(next_node.data) + ', '
            next_node = next_node.next
        s = s[:-2] + ']'
        return s

    def __len__(self) -> int:
        return self._length

    def _validate_idx(self, idx: int, append_flag: bool = False) -> None:
        if idx > self._length - (not append_flag) or idx < 0:
            raise IndexError
    
    def __getitem__(self, idx: int) -> Any:
        self._validate_idx(idx)
        next_node = self._start
        for _ in range(idx):
            next_node = next_node.next
        return next_node.data


class LinkedList(ImmutableChain, MutableSequence):

    def __setitem__(self, idx: int, data: Any) -> None:
        if idx == self._length - 1:
            self._last_node.data = data
        else:
            self._validate_idx(idx)
            current_node = self._start
            for _ in range(idx):
                current_node = current_node.next
            current_node.data = data

    def __delitem__(self, idx: int) -> None:
        self._validate_idx(idx)
        previous_node = None
        current_node = self._start
        for _ in range(idx):
            previous_node = current_node
            current_node = current_node.next
        if previous_node is not None:
            previous_node.next = current_node.next
        self._length -= 1

    def insert(self, idx: int, data: Any) -> None:
        self._validate_idx(idx, append_flag=True)
        if idx == self._length:
            self.append(data)
            return
        previous_node = None
        next_node = self._start
        for i in range(idx):
            previous_node = next_node
            next_node = next_node.next
        new_node = self.Node(data=data, links_to=next_node)
        if previous_node is None:
            self._start = new_node
        else:
            previous_node.next = new_node
        self._length += 1

    def append(self, data: Any) -> None:
        new_node = self.Node(data=data)
        if self._length == 0:
            self._start = new_node
        else:
            self._last_node.next = new_node
        self._length += 1
        self._last_node = new_node

    def extend(self, iterable: Iterable[Any]) -> None:
        if isinstance(iterable, LinkedList):
            iterable = tuple(iterable)
        super().extend(iterable)


class PriorityQueue(LinkedList):
    def __init__(self, cmp_attr: str = None):
        super().__init__()
        self.__cmp_attr = cmp_attr

    def insert(self, idx: int, data: Any) -> None:
        pass


if __name__ == '__main__':
    mylist = LinkedList()
    mylist.append(1)
    mylist.append('a')
    mylist.insert(1, 'B')
    print(mylist)
    mylist[2] = 'test'
    print(mylist)
    otherlist = LinkedList()
    otherlist.append('c')
    otherlist.append('d')
    mylist.extend(otherlist)
    print(mylist)
    mylist.extend(['e', 'f'])
    print(mylist)
    mylist.extend(mylist)
    print(mylist)
    mylist[5] = 18
    print(mylist)
