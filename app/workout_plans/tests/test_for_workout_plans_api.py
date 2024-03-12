"""
Tests for the workout_plans API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Exercise,\
    WorkoutPlan, WorkoutExercise
from workout_plans.serializers import \
    WorkoutPlanSerializer

# Helper functions


def workout_plan_url():
    return reverse('workout-plan-list')


def workout_plan_detail_url(workout_plan_id):
    return reverse('workout-plan-detail', args=[workout_plan_id])


def workout_exercise_url():
    return reverse('workout-exercise-list')


def workout_exercise_detail_url(workout_exercise_id):
    return reverse('workout-exercise-detail', args=[workout_exercise_id])


# Public API tests
class PublicWorkoutApiTests(APITestCase):
    def test_login_required_for_retrieving_workout_plans(self):
        res = self.client.get(workout_plan_url())
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_required_for_retrieving_workout_exercises(self):
        res = self.client.get(workout_exercise_url())
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


# Private API tests
class PrivateWorkoutApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@example.com', 'testpass')
        self.client.force_authenticate(self.user)

    def test_retrieve_workout_plans(self):
        WorkoutPlan.objects.create(user=self.user, title='Cutting',
                                   frequency=3, session_duration=60)
        WorkoutPlan.objects.create(user=self.user, title='Bulking',
                                   frequency=5, session_duration=90)

        res = self.client.get(workout_plan_url())
        workout_plans = WorkoutPlan.objects.filter(
            user=self.user).order_by('-title')
        serializer = WorkoutPlanSerializer(workout_plans, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_workout_plans_limited_to_user(self):
        other_user = get_user_model().objects.create_user(
            'other@example.com', 'password123')
        WorkoutPlan.objects.create(user=other_user, title='Cardio',
                                   frequency=5, session_duration=30)
        workout_plan = WorkoutPlan.objects.create(
            user=self.user, title='Strength',
            frequency=4, session_duration=45)

        res = self.client.get(workout_plan_url())

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['id'], workout_plan.id)

    def test_retrieve_workout_plan_detail(self):
        """Test retrieving a single workout plan detail"""
        workout_plan = WorkoutPlan.objects.create(
            user=self.user, title='Detail Plan',
            frequency=3, session_duration=45
        )
        url = workout_plan_detail_url(workout_plan.id)
        res = self.client.get(url)

        serializer = WorkoutPlanSerializer(workout_plan)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_workout_plan_detail_unauthorized(self):
        """unauthorized user cannot
         retrieve another user's workout plan"""
        other_user = get_user_model().objects.create_user(
            'otheruser@example.com', 'testpass')
        workout_plan = WorkoutPlan.objects.create(
            user=other_user, title='Other Plan',
            frequency=3, session_duration=30
        )
        url = workout_plan_detail_url(workout_plan.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_workout_plan_with_invalid_data(self):
        """Test creating a new workout plan with invalid data fails"""
        payload = {
            'title': '',  # Invalid title
            'frequency': -1,  # Invalid frequency
            'session_duration': 0  # Invalid session duration
        }
        res = self.client.post(workout_plan_url(), payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_nonexistent_workout_plan(self):
        """Test updating a non-existent workout plan"""
        url = workout_plan_detail_url(9999)  # unlikely to exist
        payload = {'title': 'Updated',
                   'frequency': 4, 'session_duration': 75}
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_workout_plans_sorted_by_title(self):
        """Test retrieving workout plans sorted by title"""
        WorkoutPlan.objects.create(user=self.user,
                                   title='Alpha Plan', frequency=2,
                                   session_duration=30)
        WorkoutPlan.objects.create(user=self.user,
                                   title='Beta Plan',
                                   frequency=5, session_duration=45)

        res = self.client.get(workout_plan_url(), {'ordering': 'title'})

        workout_plans = \
            WorkoutPlan.objects.filter(user=self.user).order_by('title')
        serializer = WorkoutPlanSerializer(workout_plans, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_workout_exercise(self):
        """Test creating workout exercise"""
        workout_plan = WorkoutPlan.objects.create(
            user=self.user, title='Test Plan', frequency=3,
            session_duration=60)
        exercise = Exercise.objects.create(
            name='Push Up', description='Push up description',
            instructions='Do a push up')
        payload = {
            'workout_plan': workout_plan.id,
            'exercise': exercise.id,
            'sets': 3,
            'repetitions': 10,
            'duration': 60
        }
        res = self.client.post(workout_exercise_url(), payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        workout_exercises = \
            WorkoutExercise.objects.filter(workout_plan=workout_plan)
        self.assertTrue(workout_exercises.exists())
        workout_exercise = workout_exercises[0]
        self.assertEqual(workout_exercise.exercise, exercise)

    def test_list_workout_exercise(self):
        """Test listing workout exercises"""
        workout_plan = WorkoutPlan.objects.create(
            user=self.user, title='Plan 1',
            frequency=3, session_duration=60)
        exercise = Exercise.objects.create(
            name='Squat', description='Squat description',
            instructions='Do a squat')
        WorkoutExercise.objects.create(
            workout_plan=workout_plan, exercise=exercise,
            sets=4, repetitions=15, duration=75)
        res = self.client.get(workout_exercise_url())
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['exercise'], exercise.id)

    def test_retrieve_workout_exercise_detail(self):
        """Test retrieving a single workout exercise detail"""
        workout_plan = WorkoutPlan.objects.create(
            user=self.user, title='Plan Detail', frequency=3,
            session_duration=45)
        exercise = Exercise.objects.create(
            name='Pull Up', description='Pull up description',
            instructions='Do a pull up')
        workout_exercise = \
            WorkoutExercise.objects.create(
                workout_plan=workout_plan, exercise=exercise,
                sets=3, repetitions=12, duration=60)
        url = workout_exercise_detail_url(workout_exercise.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['id'], workout_exercise.id)
        self.assertEqual(res.data['exercise'], exercise.id)

    def test_update_workout_exercise(self):
        """Test updating a workout exercise"""
        workout_plan = \
            WorkoutPlan.objects.create(
                user=self.user, title='Update Plan',
                frequency=3, session_duration=45)
        exercise = Exercise.objects.create(
            name='Jumping Jacks',
            description='Jumping Jacks description',
            instructions='Do jumping jacks')
        workout_exercise = WorkoutExercise.objects.create(
            workout_plan=workout_plan, exercise=exercise,
            sets=3, repetitions=10, duration=30)
        payload = {
            'sets': 5,
            'repetitions': 20,
            'duration': 45
        }
        url = workout_exercise_detail_url(workout_exercise.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        workout_exercise.refresh_from_db()
        self.assertEqual(workout_exercise.sets, 5)
        self.assertEqual(workout_exercise.repetitions, 20)
        self.assertEqual(workout_exercise.duration, 45)

    def test_delete_workout_exercise(self):
        """Test deleting a workout exercise"""
        workout_plan = WorkoutPlan.objects.create(
            user=self.user, title='Delete Plan',
            frequency=3, session_duration=30)
        exercise = Exercise.objects.create(
            name='Burpee', description='Burpee description',
            instructions='Do a burpee')
        workout_exercise = WorkoutExercise.objects.create(
            workout_plan=workout_plan, exercise=exercise,
            sets=4, repetitions=12, duration=45)
        url = workout_exercise_detail_url(workout_exercise.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            WorkoutExercise.objects.filter(id=workout_exercise.id).exists())
