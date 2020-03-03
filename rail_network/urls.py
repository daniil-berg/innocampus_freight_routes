from django.urls import path
from . import views, views_api

urlpatterns = [
    path('', views.graph_map, name='graph_map'),
    path('api/nodes/<int:pk>/', views_api.NodeRetrieveUpdateDestroyAPIView.as_view()),
    path('api/nodes/', views_api.NodeListCreateAPIView.as_view()),
    path('api/links/<int:pk>/', views_api.LinkRetrieveUpdateDestroyAPIView.as_view()),
    path('api/links/', views_api.LinkListCreateAPIView.as_view()),
    path('api/shortest_path/', views_api.shortest_path),
]
