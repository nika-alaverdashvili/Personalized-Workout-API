"""
Views for the workout_plans API.
"""

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiExample,
    OpenApiTypes,
)

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


@extend_schema_view(
    create=extend_schema(
        description="Create a new Workout Plan.",
        request=OpenApiTypes.OBJECT,
        examples=[
            OpenApiExample(
                name="Create Workout Plan Example",
                summary="Example create request",
                value={
                    "user": 0,
                    "title": "Beginner Fitness Plan",
                    "frequency": 3,
                    "goal": "Lose weight",
                    "session_duration": 60,
                    "create_workout_exercises": []
                },
                request_only=True,
            ),
        ],
        responses={201: WorkoutPlanSerializer},
    ),
    update=extend_schema(
        description="Update an existing Workout Plan.",
        request=OpenApiTypes.OBJECT,
        examples=[
            OpenApiExample(
                name="Update Workout Plan Example",
                summary="Example update request",
                value={
                    "user": 0,
                    "title": "Advanced Fitness Plan",
                    "frequency": 5,
                    "goal": "Build muscle",
                    "session_duration": 90,
                    "create_workout_exercises": []
                },
                request_only=True,
            ),
        ],
        responses={200: WorkoutPlanSerializer},
    ),
    partial_update=extend_schema(
        description="Partially update an existing Workout Plan.",
        request=OpenApiTypes.OBJECT,
        examples=[
            OpenApiExample(
                name="Partial Update Workout Plan Example",
                summary="Example partial update request",
                value={
                    "user": 0,
                    "title": "Advanced Fitness Plan",
                    "frequency": 5,
                    "goal": "Build muscle",
                    "session_duration": 90,
                    "create_workout_exercises": []
                },
                request_only=True,
            ),
        ],
        responses={200: WorkoutPlanSerializer},
    )
)
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
