from django.db.models import (Model,
                              CharField,
                              DateTimeField,
                              IntegerField,
                              FloatField,
                              ForeignKey,
                              OneToOneField,
                              ManyToManyField,
                              CASCADE)
from django.utils.translation import gettext_lazy as _
from django.conf import settings


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
    direct_successors = ManyToManyField(
        to='self',
        symmetrical=False,
        through='Link',
        through_fields=('tail', 'head'),
        related_name='direct_predecessors',
        related_query_name='direct_predecessor',
        verbose_name=_("Nodes linked to"),
    )

    class Meta:
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
    cost = FloatField(
        verbose_name=_("Cost"),
    )

    def __str__(self) -> str:
        return f"[{self.tail}] -> [{self.head}]"

    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("Links")


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

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
