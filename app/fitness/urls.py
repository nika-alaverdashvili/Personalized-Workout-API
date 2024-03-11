"""
URL mappings for the fitness API.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from fitness import views


router = DefaultRouter()


router.register(r'muscle-groups',
                views.MuscleGroupViewSet, basename='muscle-group')
router.register(r'exercises',
                views.ExerciseViewSet, basename='fitness-exercise')

urlpatterns = [
    path('', include(router.urls)),
]
