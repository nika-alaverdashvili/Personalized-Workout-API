from django.shortcuts import get_object_or_404
from rest_framework import viewsets


from rest_framework.permissions import IsAuthenticated
from core.models import Exercise,\
    WorkoutPlan, WorkoutExercise

from workout_plans.serializers import \
    ExerciseSerializer, WorkoutPlanSerializer,\
    WorkoutExerciseSerializer


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]


class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkoutExerciseViewSet(viewsets.ModelViewSet):
    queryset = WorkoutExercise.objects.all()
    serializer_class = WorkoutExerciseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        workout_plan_id = self.request.data.get('workout_plan')
        workout_plan = get_object_or_404(WorkoutPlan,
                                         id=workout_plan_id,
                                         user=self.request.user)
        serializer.save(workout_plan=workout_plan)
