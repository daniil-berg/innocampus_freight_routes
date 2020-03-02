from typing import Optional, Union, Tuple, Dict
from math import inf

from django.db.models import (Model,
                              CharField,
                              DateTimeField,
                              IntegerField,
                              FloatField,
                              ForeignKey,
                              OneToOneField,
                              ManyToManyField,
                              CASCADE,
                              UniqueConstraint)
from django.db.models.manager import Manager
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .priority_queue import PriorityQueue


class AbstractModel(Model):
    date_created = DateTimeField(auto_now_add=True, editable=False)
    date_updated = DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class Map(AbstractModel):
    user = ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name='maps',
        related_query_name='map',
        verbose_name=_("User"),
        editable=False,
        null=True, blank=True,
    )
    title = CharField(
        max_length=255,
        verbose_name=_("Map Title"),
        null=True, blank=True,
    )

    def __str__(self) -> str:
        if self.title:
            return self.title
        return _("Map ID %(id)s") % {'id': self.pk}

    @property
    def city_nodes_names(self):
        return dict(self.nodes.filter(city__isnull=False).values_list('id', 'city__name'))

    @property
    def adjacency_map(self):
        m = {}
        for node in self.nodes.all():
            m[node.pk] = {}
            for link in node.outgoing_links.all():
                m[node.pk][link.head_id] = link.distance
        return m

    @property
    def incidence_map(self):
        m = {}
        for node in self.nodes.all():
            m[node.pk] = {}
            for link in node.outgoing_links.all():
                m[node.pk][link.pk] = link.distance
            for link in node.incoming_links.all():
                m[node.pk][link.pk] = (-1) * link.distance
        return m

    def _node_list_and_reverse_map(self):
        node_list, rev_map = [], {}
        for idx, node in enumerate(self.nodes.all()):
            node_list.append(node.pk)
            rev_map[node.pk] = idx
        return node_list, rev_map

    def links_normalized(self):
        node_list, rev_map = self._node_list_and_reverse_map()
        links, distances = [], []
        for idx, node in enumerate(node_list):
            for link in node.outgoing_links.all():
                links.append((idx, rev_map[link.head.pk]))
                distances.append(link.distance)
            for link in node.incoming_links.all():
                links.append((rev_map[link.tail.pk], idx))
                distances.append(link.distance)
        return node_list, links, distances

    def dijkstra(self, start: Union[int, 'Node'], sum_costs: bool = True, unreachable_dist: float = inf
                 ) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
        """
        Determines shortest paths to all nodes from a specified starting node.
        Implementation of Dijkstra's algorithm.

        Args:
            start: Starting node
            sum_costs: If True, distances across edges are summed;
                       if False, path distance will be equal to maximum link distance in path.
            unreachable_dist: Value to be assigned when a node is unreachable from s

        Returns:
            2-tuple of dictionaries;
                dist - every key is a node id, every value is the minimum distance to that node from start
                pred - every key is a node id, every value is the predecessor node's id on the shortest path from start
        """
        if not isinstance(start, Node):
            start = Node.objects.get(pk=start)
        dist, pred = {}, {}
        for node in self.nodes.all():
            dist[node.pk] = unreachable_dist
            pred[node.pk] = None
        dist[start.pk] = 0
        priority_q = PriorityQueue()
        priority_q[start] = 0
        while priority_q:
            # Consider next node v in the queue
            v: Node = priority_q.next()[0]

            # Iterate through each outgoing link of node v
            for link in Link.objects.filter(tail=v):
                # Calculate alternate distance to head
                # either as the sum of link distances or als maximum link distance on the path
                alt_dist = dist[v.pk] + link.distance if sum_costs else max(dist[v.pk], link.distance)

                # If currently minimal distance to link head is greater than
                # the minimal distance to v plus the link distance
                if dist[link.head.pk] == -1 or dist[link.head.pk] > alt_dist:
                    dist[link.head.pk] = alt_dist
                    pred[link.head.pk] = v.pk
                    if link.head.pk not in priority_q:
                        priority_q[link.head] = dist[link.head.pk]
        return dist, pred

    class Meta:
        verbose_name = _("Map")
        verbose_name_plural = _("Maps")


class Node(AbstractModel):
    map = ForeignKey(
        to=Map,
        on_delete=CASCADE,
        related_name='nodes',
        related_query_name='node',
        verbose_name=_("Map"),
    )
    pos_h = IntegerField(
        verbose_name=_("Horizontal Position"),
    )
    pos_v = IntegerField(
        verbose_name=_("Vertical Position"),
    )
    # TODO: Add validation to prevent links to nodes in another map; maybe using m2m_changed signal
    direct_successors = ManyToManyField(
        to='self',
        symmetrical=False,
        through='Link',
        through_fields=('tail', 'head'),
        related_name='direct_predecessors',
        related_query_name='direct_predecessor',
        verbose_name=_("Nodes linked to"),
    )

    def link_to(self, head: Union[int, 'Node'], distance: float) -> 'Link':
        if not isinstance(head, Node):
            head = Node.objects.get(pk=head)
        return Link.objects.create(tail=self, head=head, distance=distance)

    def link_with(self, head: Union[int, 'Node'], distance: float) -> Tuple['Link', 'Link']:
        if not isinstance(head, Node):
            head = Node.objects.get(pk=head)
        link_to = Link.objects.create(tail=self, head=head, distance=distance)
        link_from = Link.objects.create(tail=head, head=self, distance=distance)
        return link_to, link_from

    class Meta:
        constraints = [
            UniqueConstraint(fields=['map', 'pos_h', 'pos_v'], name='exclusive_position'),
        ]
        verbose_name = _("Node")
        verbose_name_plural = _("Nodes")


class Link(AbstractModel):
    tail = ForeignKey(
        to=Node,
        on_delete=CASCADE,
        related_name='outgoing_links',
        related_query_name='outgoing_link',
        verbose_name=_('"from"-Node')
    )
    head = ForeignKey(
        to=Node,
        on_delete=CASCADE,
        related_name='incoming_links',
        related_query_name='incoming_link',
        verbose_name=_('"to"-Node')
    )
    distance = FloatField(
        verbose_name=_("Distance"),
    )

    def __str__(self) -> str:
        return f"[{self.tail}] -> [{self.head}]"

    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("Links")


class CityManager(Manager):
    def create_city_node(self, map_id: int, pos_v: int, pos_h: int, name: str):
        node = Node.objects.create(map_id=map_id, pos_v=pos_v, pos_h=pos_h)
        return super().create(node=node, name=name)


class City(AbstractModel):
    node = OneToOneField(
        to=Node,
        on_delete=CASCADE,
        verbose_name=_("Node"),
    )
    name = CharField(
        max_length=255,
        verbose_name=_("City name"),
        null=True, blank=True,
    )

    def __str__(self) -> str:
        if self.name:
            return self.name
        return _("City Node ID %(id)s") % {'id': self.node_id}

    def link_to(self, head: Union[int, 'Node'], distance: float) -> 'Link':
        return self.node.link_to(head=head, distance=distance)

    def link_with(self, head: Union[int, 'Node'], distance: float) -> Tuple['Link', 'Link']:
        return self.node.link_with(head=head, distance=distance)

    objects = CityManager()

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
