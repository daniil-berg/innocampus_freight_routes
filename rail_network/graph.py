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


class Graph:
    """
    A Graph object is internally stored as an adjacency matrix.

    Weighted and directed.
    """

    def __init__(self, n: int = 0, edges: List[Tuple[int, int]] = None, costs: List[AnyNumeric] = None):
        """
        Initialization with optional arguments.

        Args:
            n: Number of vertices
            edges: List of 2-tuples of integers representing vertex numbers
            costs: List of numeric values representing cost of edges; must be of the same length as edges
        """
        self.__adj_matrix = []
        for i in range(n):
            self.__adj_matrix.append([])
            for j in range(n):
                if i == j:
                    self.adj_matrix[i].append(0)
                    continue
                try:
                    e_idx = edges.index((i, j))
                    self.__adj_matrix[i].append(costs[e_idx])
                except ValueError:
                    self.__adj_matrix[i].append(inf)

    @property
    def vertex_count(self) -> int:
        """Number of vertices"""
        return len(self.__adj_matrix)

    @property
    def adj_matrix(self) -> List[List[AnyNumeric]]:
        """Adjacency matrix for the graph"""
        return self.__adj_matrix

    def get_adjacent(self, v: int) -> List[int]:
        """Returns list of vertices (indices) that have an incoming edge from v."""
        return [w for w, cost in enumerate(self.__adj_matrix[v]) if cost < inf]

    def dijkstra(self,
                 s: int,
                 sum_costs: bool = True,
                 unreachable_dist: AnyNumeric = inf) -> Tuple[List[AnyNumeric],
                                                              List[Optional[int]]]:
        """
        Determines shortest paths to all vertices from starting vertex s.
        Implementation of Dijkstra's algorithm.

        Args:
            s: Starting vertex index
            sum_costs: If True, costs across edges are summed;
                       if False, path cost will be equal to maximum edge cost.
            unreachable_dist: Value to be assigned when a vertex is unreachable from s
        """
        dist = [unreachable_dist for _ in range(self.vertex_count)]
        pred = [None for _ in range(self.vertex_count)]
        dist[s] = 0
        priority_q = PriorityQueue()
        priority_q[s] = 0
        while priority_q:
            # Consider next vertex in the queue
            v = priority_q.next()[0]

            # Iterate through the adjacent vertices of v (outgoing edges)
            for w, cost in enumerate(self.__adj_matrix[v]):
                if cost == inf:
                    continue
                # Calculate alternate distance to vertex w
                # either as the sum of edge costs or als maximum edge cost on the path
                alternate_cost = dist[v] + cost if sum_costs else max(dist[v], cost)

                # If currently minimal distance to w is greater than
                # the min distance to v plus the v-w-distance
                if dist[w] == -1 or dist[w] > alternate_cost:
                    dist[w] = alternate_cost
                    pred[w] = v
                    if w not in priority_q:
                        priority_q[w] = dist[w]
        return dist, pred
