from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Elective, Choice
from .serializers import ElectiveSerializer, ChoiceSerializer


class ElectiveListAPI(APIView):
    """GET /api/electives/ — returns all electives with seat counts."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        electives = Elective.objects.all()
        serializer = ElectiveSerializer(electives, many=True)
        return Response(serializer.data)


class ChoiceListAPI(APIView):
    """GET /api/choices/ — returns current user's choices."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        choices = Choice.objects.filter(student=request.user).order_by('priority')
        serializer = ChoiceSerializer(choices, many=True)
        return Response(serializer.data)
