from django.db import transaction
from rest_framework import serializers

from .models import Node, Link, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'date_created', 'date_updated')


class NodeSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Node
        fields = ('id', 'map', 'pos_h', 'pos_v', 'city', 'direct_successors', 'date_created', 'date_updated')

    def create(self, validated_data):
        city_data = validated_data.pop('city')
        with transaction.atomic():
            new_node = Node.objects.create(**validated_data)
            City.objects.create(node=new_node, **city_data)
        return new_node

    def update(self, instance, validated_data):
        instance.pos_h = validated_data.get('pos_h', instance.pos_h)
        instance.pos_v = validated_data.get('pos_v', instance.pos_v)
        instance.save()
        if 'city' in validated_data.keys():
            if instance.city is not None:
                instance.city.name = validated_data['city'].get('name', instance.city.name)
                instance.city.save()
            else:
                City.objects.create(node=instance, **validated_data['city'])
        return instance
