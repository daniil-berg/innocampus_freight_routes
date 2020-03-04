from math import inf

from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Map, Node, Link
from .serializers import NodeSerializer, LinkSerializer


@api_view(['GET'])
def shortest_path(request: Request) -> Response:
    start_id = request.query_params.get('start')
    end_id = request.query_params.get('end')
    if start_id is None or end_id is None:
        return Response("Both 'start' and 'end' are required", status=HTTP_400_BAD_REQUEST)
    start_id = int(start_id)
    end_id = int(end_id)

    # TODO: map_id currently defaults to last Map if none was passed!
    map_id = request.query_params.get('map', Map.objects.last().pk)
    map_obj = get_object_or_404(Map, id=map_id)

    if not Node.objects.filter(id=start_id, map=map_obj).exists():
        return Response("Node ID {} on Map ID {} does not exist".format(start_id, map_id), status=HTTP_404_NOT_FOUND)
    if not Node.objects.filter(id=end_id, map=map_obj).exists():
        return Response("Node ID {} on Map ID {} does not exist".format(end_id, map_id), status=HTTP_404_NOT_FOUND)

    algorithm = request.query_params.get('algorithm', 'dijkstra')
    if algorithm in ('dijkstra', 'a_star'):
        dist, path = map_obj.shortest_path_from_to(start=start_id, end=end_id, algorithm=algorithm)
        if dist == inf:
            dist = -1
        return Response(data={'dist': dist, 'path': path})
    else:
        return Response("Algorithm '{}' not valid or not implemented".format(algorithm), status=HTTP_400_BAD_REQUEST)


class NodeListCreateAPIView(ListCreateAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer


class NodeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer


class LinkListCreateAPIView(ListCreateAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

    def create(self, request, *args, **kwargs):
        if 'head' not in request.data or 'tail' not in request.data:
            return Response("Both 'head' and 'tail' are required", status=HTTP_400_BAD_REQUEST)
        reverse_data = request.data.copy()
        reverse_data['head'], reverse_data['tail'] = request.data['tail'], request.data['head']
        serializer = self.get_serializer(data=request.data)
        serializer_reverse = self.get_serializer(data=reverse_data)
        serializer.is_valid(raise_exception=True)
        serializer_reverse.is_valid(raise_exception=True)
        self.perform_create(serializer)
        self.perform_create(serializer_reverse)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class LinkRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        reverse_data = request.data.copy()
        reverse_data['head'], reverse_data['tail'] = request.data['tail'], request.data['head']
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer_reverse = self.get_serializer(instance.reverse, data=reverse_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer_reverse.is_valid(raise_exception=True)
        self.perform_update(serializer)
        self.perform_update(serializer_reverse)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance: Link = self.get_object()
        with transaction.atomic():
            self.perform_destroy(instance.reverse)
            self.perform_destroy(instance)
        return Response(status=HTTP_204_NO_CONTENT)
