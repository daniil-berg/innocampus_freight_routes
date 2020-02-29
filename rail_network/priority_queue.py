from typing import Any, Iterable
from collections.abc import Sequence, MutableSequence


class ImmutableChain(Sequence):
    class Node:
        def __init__(self, data: Any, links_to: 'ImmutableChain.Node' = None):
            self.data = data
            self.next = links_to

    def __init__(self, repr_sep: str = ' -> '):
        self._start = None
        self._length = 0
        self._last_node = None
        self._repr_sep = repr_sep

    def __repr__(self) -> str:
        s = '('
        next_node = self._start
        for _ in range(self._length):
            s += repr(next_node.data) + self._repr_sep
            next_node = next_node.next
        s = s[:-len(self._repr_sep)] + ')'
        return s

    def __len__(self) -> int:
        return self._length

    def _validate_idx(self, idx: int, append_flag: bool = False) -> None:
        if idx > self._length - (not append_flag) or idx < 0:
            raise IndexError
    
    def __getitem__(self, idx: int) -> Any:
        if idx == -1:
            return self._last_node.data
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

    def append(self, data: Any) -> None:
        new_node = self.Node(data=data)
        if self._length == 0:
            self._start = new_node
        else:
            self._last_node.next = new_node
        self._length += 1
        self._last_node = new_node

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

    def extend(self, iterable: Iterable[Any]) -> None:
        if isinstance(iterable, LinkedList):
            iterable = tuple(iterable)
        super().extend(iterable)


class PriorityQueue(ImmutableChain):
    def __init__(self, cmp_attr: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cmp_attr = cmp_attr

    def priority_higher(self, of: Any, than: Any) -> bool:
        if self.__cmp_attr is None:
            return of > than
        if not (hasattr(of, self.__cmp_attr) and hasattr(than, self.__cmp_attr)):
            raise AttributeError
        return getattr(of, self.__cmp_attr) > getattr(than, self.__cmp_attr)

    def put(self, obj: Any) -> None:
        previous_node = None
        next_node = self._start
        while next_node is not None and not self.priority_higher(obj, next_node.data):
            previous_node = next_node
            next_node = next_node.next
        new_node = self.Node(data=obj, links_to=next_node)
        if previous_node is None:
            self._start = new_node
        else:
            previous_node.next = new_node
        self._length += 1
        if next_node is None:
            self._last_node = new_node


if __name__ == '__main__':
    q = PriorityQueue()
    q.put(2)
    q.put(5)
    q.put(3)
    q.put(3)
    print(q)
    print(q.index(2))
    print(q[-1])
