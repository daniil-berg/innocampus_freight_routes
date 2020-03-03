from rest_framework import serializers

from .models import Node, Link, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'date_created', 'date_updated')

    def create(self, validated_data):
        city_data = validated_data.pop('city')
        City.objects.create_city_node(**validated_data)

    # def update(self, instance, validated_data):


class NodeSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Node
        fields = ('id', 'map', 'pos_h', 'pos_v', 'city', 'direct_successors', 'date_created', 'date_updated')

