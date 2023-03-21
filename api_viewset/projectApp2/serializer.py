from rest_framework import serializers
from .models import Car


class CarSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    model_name = serializers.CharField(max_length=30)
    color = serializers.CharField(max_length=20)

    def create(self, validated_data):
        return Car.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.model_name = validated_data["model_name"]
        instance.color = validated_data["color"]
        instance.save()
        return instance
