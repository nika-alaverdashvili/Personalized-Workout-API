"""
URL mappings for the workout_plans API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from workout_plans import views

router = DefaultRouter()

router.register(r'workout-plans',
                views.WorkoutPlanViewSet, basename='workout-plan')

router.register(r'plan-exercises',
                views.ExerciseViewSet, basename='plan-exercise')

router.register(r'workout-exercises',
                views.WorkoutExerciseViewSet, basename='workout-exercise')


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
]
