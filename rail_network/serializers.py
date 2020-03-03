from rest_framework import serializers

from .models import Node, Link, City


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ('id', 'map', 'pos_h', 'pos_v', 'direct_successors', 'date_created', 'date_updated')


class CitySerializer(serializers.ModelSerializer):
    node = NodeSerializer()

    class Meta:
        model = City
        fields = ('id', 'name', 'node', 'date_created', 'date_updated')

    def create(self, validated_data):
        City.objects.create_city_node(**validated_data)
