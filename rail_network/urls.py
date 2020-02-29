from django.urls import path
from . import views

urlpatterns = [
    path('', views.new_map, name='new_map'),
]
