from rest_framework import serializers
from .models import Allotment


class AllotmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_usn = serializers.CharField(source='student.usn', read_only=True)
    elective_name = serializers.CharField(source='elective.name', read_only=True)
    elective_code = serializers.CharField(source='elective.code', read_only=True)

    class Meta:
        model = Allotment
        fields = ['id', 'student_name', 'student_usn', 'elective_name', 'elective_code', 'allotted_at']
