from rest_framework import serializers
from .models import Elective, Choice


class ElectiveSerializer(serializers.ModelSerializer):
    fill_percentage = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()

    class Meta:
        model = Elective
        fields = ['id', 'name', 'code', 'total_seats', 'available_seats', 'fill_percentage', 'status']


class ChoiceSerializer(serializers.ModelSerializer):
    elective_name = serializers.CharField(source='elective.name', read_only=True)
    elective_code = serializers.CharField(source='elective.code', read_only=True)

    class Meta:
        model = Choice
        fields = ['id', 'elective', 'elective_name', 'elective_code', 'priority', 'submitted_at']
        read_only_fields = ['submitted_at']
