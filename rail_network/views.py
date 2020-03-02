from django.shortcuts import render

from .models import Map


def new_map(request):
    init_nodes, init_links = [], []
    if Map.objects.all().count() != 0:
        map_obj = Map.objects.first()
        init_nodes = map_obj.cytoscape_nodes_list
        init_links = map_obj.cytoscape_links_list
    context = {
        'init_nodes': init_nodes,
        'init_links': init_links,
    }
    return render(request, 'rail_network/new_map.html', context=context)
