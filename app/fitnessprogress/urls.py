"""
Urls for the fitnessprogress APIs
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from fitnessprogress import views

router = DefaultRouter()
router.register(r'fitness-progress',
                views.FitnessProgressViewSet,
                basename='fitness-progress')

urlpatterns = [
    path('', include(router.urls)),
]
