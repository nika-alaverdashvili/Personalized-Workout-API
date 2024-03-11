"""
Tests for the fitness API.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import MuscleGroup, Exercise
from fitness.serializers import (MuscleGroupSerializer,
                                 ExerciseSerializer,
                                 )
from django.test import TestCase


def muscle_group_url():
    """Return URL for muscle groups"""
    return reverse('muscle-group-list')


def exercise_url():
    """Return URL for exercises"""
    return reverse('fitness-exercise-list')  # Update based on new 'basename'


def muscle_group_detail_url(muscle_group_id):
    """Return muscle group detail URL"""
    return reverse('muscle-group-detail', args=[muscle_group_id])


def exercise_detail_url(exercise_id):
    """Return exercise detail URL"""
    return reverse('fitness-exercise-detail', args=[exercise_id])


class PublicApiTests(TestCase):
    """Test unauthenticated API access"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_muscle_groups(self):
        MuscleGroup.objects.create(name='Biceps',
                                   description='Front of the upper arm')
        MuscleGroup.objects.create(name='Triceps',
                                   description='Back of the upper arm')

        res = self.client.get(muscle_group_url())

        expected = MuscleGroup.objects.all().order_by('id')
        serializer = MuscleGroupSerializer(expected, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_exercises(self):
        muscle_group = \
            MuscleGroup.objects.create(name='Chest',
                                       description='Chest muscle group')
        Exercise.objects.create(
            name='Push Up',
            description='Push up exercise',
            instructions='Start in a plank position and push down'
        ).target_muscles.set([muscle_group])

        res = self.client.get(exercise_url())
        expected = Exercise.objects.all().order_by('name')
        serializer = ExerciseSerializer(expected, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class AdminApiTests(TestCase):
    """Test API requests that require admin permissions"""

    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            'admin@example.com',
            'password'
        )
        self.client.force_authenticate(self.admin_user)
        self.muscle_group = \
            MuscleGroup.objects.create(name='Legs',
                                       description='Lower body muscles')

    def test_create_muscle_group(self):
        """Test creating a muscle group"""
        payload = {'name': 'Shoulders', 'description': 'Shoulder muscles'}
        res = self.client.post(muscle_group_url(), payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        muscle_group = MuscleGroup.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(muscle_group, key))

    def test_create_exercise(self):
        """Test creating an exercise"""
        payload = {
            'name': 'Deadlift',
            'description': 'A compound exercise',
            'instructions': 'Lift the barbell from the ground to hip level',
            'target_muscles': [self.muscle_group.id]
        }
        res = self.client.post(exercise_url(), payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        exercise = Exercise.objects.get(id=res.data['id'])
        associated_muscle_groups = exercise.target_muscles.all()

        print("Expected Muscle Group:", self.muscle_group)
        print("Associated Muscle Groups:", associated_muscle_groups)

        self.assertIn(self.muscle_group, associated_muscle_groups)

    def test_partial_update_muscle_group(self):
        """Test partially updating a muscle group's detail using patch"""
        muscle_group = \
            MuscleGroup.objects.create(name='Core',
                                       description='Core muscles')

        payload = {'name': 'Core Strength'}
        url = muscle_group_detail_url(muscle_group.id)
        self.client.patch(url, payload)

        muscle_group.refresh_from_db()
        self.assertEqual(muscle_group.name, payload['name'])

    def test_full_update_exercise(self):
        """Test updating an exercise with put"""
        exercise = Exercise.objects.create(
            name='Barbell Curl',
            description='Curl exercise for biceps',
            instructions='Curl the barbell while standing',
        )
        exercise.target_muscles.add(self.muscle_group)
        payload = {
            'name': 'Hammer Curl',
            'description': 'Curl exercise for forearm and biceps',
            'instructions': 'Curl the dumbbell with hands in neutral position',
            'target_muscles': [self.muscle_group.id]
        }

        url = exercise_detail_url(exercise.id)
        self.client.put(url, payload, format='json')

        exercise.refresh_from_db()
        self.assertEqual(exercise.name, payload['name'])
        self.assertEqual(exercise.description, payload['description'])
        self.assertEqual(exercise.instructions, payload['instructions'])
