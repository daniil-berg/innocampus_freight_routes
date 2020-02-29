from django.shortcuts import render


def new_map(request):
    return render(request, 'rail_network/new_map.html')
