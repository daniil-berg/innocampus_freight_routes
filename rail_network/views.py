from django.shortcuts import render

from .models import Map


def new_map(request):
    init_elements = []
    if Map.objects.all().count() != 0:
        map_obj = Map.objects.first()
        init_elements = map_obj.cytoscape_elements_list
    context = {
        'init_elements': init_elements,
    }
    return render(request, 'rail_network/new_map.html', context=context)
