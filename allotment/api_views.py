from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Allotment
from .serializers import AllotmentSerializer
from .algorithm import run_allotment


class AllotmentResultsAPI(APIView):
    """GET /api/allotment/results/ — returns all allotment results."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        allotments = Allotment.objects.select_related('student', 'elective').all()
        serializer = AllotmentSerializer(allotments, many=True)
        return Response(serializer.data)


class RunAllotmentAPI(APIView):
    """POST /api/allotment/run/ — triggers the allotment algorithm (admin only)."""
    permission_classes = [IsAdminUser]

    def post(self, request):
        result = run_allotment()
        return Response({
            'status': 'success',
            'allotted': result['allotted'],
            'unallotted': result['unallotted'],
            'total': result['total'],
        })
