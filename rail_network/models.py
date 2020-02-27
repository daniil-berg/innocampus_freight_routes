from django.db.models import (Model,
                              CharField,
                              DateTimeField,
                              IntegerField,
                              ForeignKey,
                              OneToOneField,
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

    def __str__(self):
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

    class Meta:
        verbose_name = _("Node")
        verbose_name_plural = _("Nodes")


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

    def __str__(self):
        if self.name:
            return self.name
        return _("City Node ID %(id)s") % {'id': self.node_id}

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
