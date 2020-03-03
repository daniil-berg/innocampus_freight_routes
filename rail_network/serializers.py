from rest_framework import serializers

from .models import Node, Link, City


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    node = NodeSerializer()

    class Meta:
        model = City
        fields = ('id', 'name', 'node', )
