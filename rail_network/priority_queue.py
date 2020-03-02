from typing import TypeVar, List, Tuple, Optional
from collections.abc import MutableMapping
from math import inf


AnyNumeric = TypeVar('AnyNumeric', int, float)


class PriorityQueue(MutableMapping):
    """
    PriorityQueue implemented as a sort of mix between sequence and mapping.
    Container for 2-tuples of key-object and corresponding value.
    Always sorted by value.
    """
    # TODO: Use https://github.com/DanielStutzbach/heapdict instead! list.insert() is extremely inefficient

    def __init__(self):
        """Priority Queue instances are initialized empty."""
        self.__queue = []

    def __repr__(self):
        return repr(self.__queue)

    def __getitem__(self, item):
        """Emulates dict-like access to item-values"""
        for key, value in self.__queue:
            if key == item:
                return value
        raise KeyError

    def pos(self, item, get_value=False):
        """Returns position of item in queue and optionally its value."""
        for idx, (key, value) in enumerate(self.__queue):
            if key == item:
                return idx, value if get_value else idx
        raise KeyError

    def __bin_ins(self, start: int, stop: int, key, value):
        """Recursive binary insert of new key-value-pairs into queue to maintain order"""
        if stop - start == 0:
            # Queue sub-section is empty
            self.__queue.insert(start, (key, value))
            return
        elif stop - start == 1:
            # Only one element in queue sub-section
            # Insert new element accordingly
            if value < self.__queue[start][1]:
                self.__queue.insert(start, (key, value))
            else:
                self.__queue.insert(stop, (key, value))
            return

        middle = (start + stop) // 2
        if value < self.__queue[middle][1]:
            self.__bin_ins(start, middle, key, value)
        else:
            self.__bin_ins(middle, stop, key, value)
        return

    def __setitem__(self, key, value):
        """Emulates dict-like key-value-assignment; updates queue order if necessary"""
        try:
            current_pos, current_val = self.pos(key, get_value=True)
        except KeyError:
            current_pos, current_val = None, None

        if current_pos:
            if current_val == value:
                return
            else:
                del self.__queue[current_pos]
        self.__bin_ins(0, len(self.__queue), key, value)

    def __delitem__(self, key):
        """Emulates dict-like key deletion"""
        pos = self.pos(key)
        assert isinstance(pos, int)
        del self.__queue[pos]

    def __iter__(self):
        """Generator iterator over keys"""
        for key, _ in self.__queue:
            yield key

    def __len__(self):
        return len(self.__queue)

    def next(self):
        """Pops item-value-pair with lowest value"""
        return self.__queue.pop(0)

    def keys(self):
        return [key for key, _ in self.__queue]

    def values(self):
        return [value for _, value in self.__queue]

    def items(self):
        return self.__queue.copy()

    def get(self, key, default=None):
        """Emulates dict-like get method with default-fallback"""
        try:
            return self[key]
        except KeyError:
            return default
