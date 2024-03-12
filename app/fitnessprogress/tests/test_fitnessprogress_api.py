"""
Tests for the FitnessProgress API.
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import FitnessProgress
from decimal import Decimal
from datetime import date
from datetime import timedelta


def fitness_progress_list_url():
    """Return URL for fitness progress list"""
    return reverse('fitness-progress-list')


def fitness_progress_detail_url(fp_id):
    """Return fitness progress detail URL"""
    return reverse('fitness-progress-detail', args=[fp_id])


class PublicFitnessProgressApiTests(TestCase):
    """Test unauthenticated API access to FitnessProgress"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required_for_list(self):
        """Test that login is required to
         access the FitnessProgress list"""
        res = self.client.get(fitness_progress_list_url())
        self.assertEqual(res.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_login_required_for_detail(self):
        """Test that login is required for
         accessing a FitnessProgress detail"""
        sample_id = 1
        res = self.client.get(fitness_progress_detail_url(sample_id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateFitnessProgressApiTests(TestCase):
    """Test authenticated API access to FitnessProgress."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='user@example.com', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.fitness_progress = FitnessProgress.objects.create(
            user=self.user, date=date.today() - timedelta(days=1),
            weight=Decimal('70.0')
        )

    def test_create_fitness_progress(self):
        """Test creating a new FitnessProgress record."""
        payload = {
            'date': (date.today()).isoformat(),
            'weight': '75.0',
            'goal_weight': '65.0',
            'achieved_goals': 'Ran 10km',
            'notes': 'Felt great afterwards',
            'exercise_duration': 90,
            'calories_burned': 500,
            'mood': 'Happy'
        }
        res = self.client.post(fitness_progress_list_url(), payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_fitness_progress(self):
        """Test updating an existing FitnessProgress record."""
        update_payload = {
            'weight': '68.0',
            'notes': 'Feeling even better',
            'exercise_duration': 60
        }
        url = fitness_progress_detail_url(self.fitness_progress.id)
        res = self.client.patch(url, update_payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_fitness_progress(self):
        """Test deleting a FitnessProgress record."""
        url = fitness_progress_detail_url(self.fitness_progress.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code,
                         status.HTTP_204_NO_CONTENT)
        self.assertFalse(FitnessProgress.objects.filter(
            id=self.fitness_progress.id).exists())
