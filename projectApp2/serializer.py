from rest_framework import serializers

from projectApp3.models import CarPart
from .models import Car


class CarSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    model_name = serializers.CharField(max_length=30)
    color = serializers.CharField(max_length=20)
    parts_available = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=CarPart.objects.all())

    def create(self, validated_data):
        return Car.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.model_name = validated_data["model_name"]
        instance.color = validated_data["color"]
        print(validated_data)
        if validated_data.get("parts_available", False):
            instance.parts_available.clear()
            for car_part in validated_data['parts_available']:
                instance.parts_available.add(car_part)
        instance.save()
        return instance
