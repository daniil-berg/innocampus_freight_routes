from django.db import transaction
from rest_framework import serializers

from .models import Node, Link, City


class CitySerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    date_updated = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = City
        fields = ('id', 'name', 'date_created', 'date_updated')


class NodeSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    date_created = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    date_updated = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = Node
        fields = ('id', 'map', 'pos_h', 'pos_v', 'city', 'date_created', 'date_updated')

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


class LinkSerializer(serializers.ModelSerializer):
    tail = NodeSerializer()
    head = NodeSerializer()
    date_created = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    date_updated = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = Link
        fields = ('id', 'distance', 'tail', 'head', 'date_created', 'date_updated')

    def create(self, validated_data):
        return Link.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.distance = validated_data.get('distance', instance.distance)
        instance.save()
        return instance
