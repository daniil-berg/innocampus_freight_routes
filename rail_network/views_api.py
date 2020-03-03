from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Map, Node, Link
from .serializers import NodeSerializer, LinkSerializer


@api_view(['GET'])
def shortest_path(request: Request) -> Response:
    start_id = request.query_params.get('start')
    end_id = request.query_params.get('end')
    if start_id is None or end_id is None:
        return Response(status=HTTP_400_BAD_REQUEST)
    try:
        start_id = int(start_id)
        end_id = int(end_id)
    except ValueError:
        return Response(status=HTTP_400_BAD_REQUEST)
    # TODO: map_id currently defaults to last Map if none was passed!
    map_id = request.query_params.get('map', Map.objects.last().pk)
    map_obj = get_object_or_404(Map, id=map_id)
    algorithm = request.query_params.get('algorithm', 'dijkstra')
    if algorithm == 'dijkstra':
        dist, path = map_obj.dijkstra_from_to(start=start_id, end=end_id)
        return Response(data={'dist': dist, 'path': path})
    else:
        return Response(status=HTTP_400_BAD_REQUEST)


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
