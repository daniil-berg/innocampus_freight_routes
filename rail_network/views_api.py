from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Map, Node, City
from .serializers import NodeSerializer


# TODO: Here, as with the regular views, everything returned is always related to the last Map object

class NodeListCreateAPIView(ListCreateAPIView):
    queryset = Node.objects.filter(map=Map.objects.last())
    serializer_class = NodeSerializer


class NodeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Node.objects.filter(map=Map.objects.last())
    serializer_class = NodeSerializer
