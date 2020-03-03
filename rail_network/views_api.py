from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Map, Node, Link, City
from .serializers import NodeSerializer, LinkSerializer


class NodeListCreateAPIView(ListCreateAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer


class NodeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer


class LinkListCreateAPIView(ListCreateAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class LinkRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
