"""
Views for the fitnessprogress APIs
"""


from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import FitnessProgress
from fitnessprogress.serializers import FitnessProgressSerializer


class FitnessProgressViewSet(viewsets.ModelViewSet):
    queryset = FitnessProgress.objects.all()
    serializer_class = FitnessProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FitnessProgress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
