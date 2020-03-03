from django.urls import path
from . import views, views_api

urlpatterns = [
    path('', views.graph_map, name='graph_map'),
    path('api/cities/', views_api.CityListCreateAPIView.as_view()),
]
