from django.shortcuts import render

from .models import Map


def new_map(request):
    """
    Currently, this just loads the Map (i.e. Graph) last saved in the database into the context in Cytoscape.js format
    """
    init_elements = []
    if Map.objects.all().count() != 0:
        map_obj = Map.objects.last()
        init_elements = map_obj.cytoscape_elements_list
    context = {
        'init_elements': init_elements,
    }
    return render(request, 'rail_network/new_map.html', context=context)
