from rest_framework.generics import ListCreateAPIView

from .models import Map, City
from .serializers import CitySerializer


# TODO: Here, as with the regular views, everything returned is always related to the last Map object

class CityListCreateAPIView(ListCreateAPIView):
    queryset = City.objects.filter(node__map=Map.objects.last())
    serializer_class = CitySerializer
