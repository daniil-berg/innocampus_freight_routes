from django.db.models import (Model,
                              CharField,
                              DateTimeField,
                              ForeignKey,
                              CASCADE)
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
        verbose_name="User",
        editable=False,
    )
    title = CharField(
        max_length=255,
        verbose_name="Map Title"
    )


class Node(AbstractModel):
    pass


class City(AbstractModel):
    pass
