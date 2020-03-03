from django.shortcuts import render

from .models import Map


def graph_map(request):
    """
    TODO: Currently, this just loads the Map (i.e. Graph) last saved in the database into the context in Cytoscape.js format
    """
    if Map.objects.all().count() != 0:
        map_obj = Map.objects.last()
        init_elements = map_obj.cytoscape_elements_list
    else:
        map_obj = Map.objects.create()
        init_elements = []
    context = {
        'init_elements': init_elements,
        'map_id': map_obj.pk,
    }
    return render(request, 'rail_network/map.html', context=context)
