"""
Views for the fitness APIs
"""


from rest_framework import viewsets, permissions
from core.models import MuscleGroup, Exercise
from fitness.serializers import MuscleGroupSerializer, ExerciseSerializer


class MuscleGroupViewSet(viewsets.ModelViewSet):
    queryset = MuscleGroup.objects.all()
    serializer_class = MuscleGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all().order_by('name')
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
