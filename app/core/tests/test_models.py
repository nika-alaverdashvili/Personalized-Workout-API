"""
Tests for models.
"""
from decimal import Decimal
from datetime import date

from django.db import IntegrityError

from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import MuscleGroup, Exercise, WorkoutPlan,\
    WorkoutExercise, FitnessProgress


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = \
                get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class MuscleGroupModelTests(TestCase):

    def test_muscle_group_str(self):
        """Test the muscle group string representation"""
        muscle_group = MuscleGroup.objects.create(
            name='Biceps',
            description='Front of the upper arm'
        )
        self.assertEqual(str(muscle_group), muscle_group.name)


class ExerciseModelTests(TestCase):

    def setUp(self):
        """Set up for testing"""
        self.muscle_group = MuscleGroup.objects.create(
            name='Triceps',
            description='Back of the upper arm'
        )

    def test_exercise_str(self):
        """Test the exercise string representation"""
        exercise = Exercise.objects.create(
            name='Tricep Dips',
            description='Dips to work the triceps',
            instructions='Perform dips on parallel '
                         'bars with a focus on the triceps'
        )
        exercise.target_muscles.add(self.muscle_group)

        self.assertEqual(str(exercise), exercise.name)

    def test_exercise_target_muscles(self):
        """Test the target muscles are correctly assigned to exercises"""
        exercise = Exercise.objects.create(
            name='Pull-up',
            description='Upper body compound pull exercise.',
            instructions='Hang from a bar and pull yourself'
                         ' up until your chin passes the bar.'
        )
        exercise.target_muscles.add(self.muscle_group)

        self.assertIn(self.muscle_group, exercise.target_muscles.all())


class WorkoutPlanModelTests(TestCase):

    def setUp(self):
        """Set up for testing WorkoutPlan and WorkoutExercise models."""
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123'
        )

    def test_workout_plan_str(self):
        """Test the workout plan string representation."""
        workout_plan = WorkoutPlan.objects.create(
            user=self.user,
            title='My Workout Plan',
            frequency=5,
            goal='Increase muscle strength',
            session_duration=60
        )
        self.assertEqual(str(workout_plan),
                         f'{workout_plan.title} - {self.user.email}')

    def test_workout_plan_fields(self):
        """Test creating a workout plan with specific fields."""
        workout_plan = WorkoutPlan.objects.create(
            user=self.user,
            title='Fat Loss Plan',
            frequency=3,
            goal='Lose 5kg',
            session_duration=45
        )
        self.assertEqual(workout_plan.user, self.user)
        self.assertEqual(workout_plan.title, 'Fat Loss Plan')
        self.assertEqual(workout_plan.frequency, 3)
        self.assertEqual(workout_plan.goal, 'Lose 5kg')
        self.assertEqual(workout_plan.session_duration, 45)


class WorkoutExerciseModelTests(TestCase):

    def setUp(self):
        """Set up for testing WorkoutPlan and WorkoutExercise models."""
        self.user = get_user_model().objects.create_user(
            email='user2@example.com',
            password='testpass123'
        )
        self.workout_plan = WorkoutPlan.objects.create(
            user=self.user,
            title='Strength Training',
            frequency=4,
            session_duration=90
        )
        self.muscle_group = MuscleGroup.objects.create(
            name='Chest',
            description='Pectoral muscles'
        )
        self.exercise = Exercise.objects.create(
            name='Bench Press',
            description='Chest press exercise for building muscle',
            instructions='Lie on bench and press barbell upward'
        )
        self.exercise.target_muscles.add(self.muscle_group)

    def test_workout_exercise_str(self):
        """Test the workout exercise string representation."""
        workout_exercise = WorkoutExercise.objects.create(
            workout_plan=self.workout_plan,
            exercise=self.exercise,
            sets=4,
            repetitions=10,
            duration=120
        )
        self.assertEqual(str(workout_exercise),
                         f'{self.exercise.name} - 4 sets of 10')

    def test_workout_exercise_fields(self):
        """Test creating a workout exercise with specific fields."""
        workout_exercise = WorkoutExercise.objects.create(
            workout_plan=self.workout_plan,
            exercise=self.exercise,
            sets=3,
            repetitions=12,
            duration=90
        )
        self.assertEqual(workout_exercise.workout_plan, self.workout_plan)
        self.assertEqual(workout_exercise.exercise, self.exercise)
        self.assertEqual(workout_exercise.sets, 3)
        self.assertEqual(workout_exercise.repetitions, 12)
        self.assertEqual(workout_exercise.duration, 90)


class FitnessProgressModelTests(TestCase):

    def setUp(self):
        """Set up for testing FitnessProgress model."""
        self.user = get_user_model().objects.create_user(
            email='user3@example.com',
            password='testpass123'
        )

    def test_fitness_progress_str(self):
        """Test the fitness progress string representation."""
        fitness_progress = FitnessProgress.objects.create(
            user=self.user,
            date=date(2022, 1, 1),
            weight=Decimal('180.00'),
            goal_weight=Decimal('160.00'),
            achieved_goals='Run 5km without stopping',
            notes='Felt great after the run.'
        )
        self.assertEqual(str(fitness_progress),
                         f'2022-01-01 - {self.user.email}')

    def test_fitness_progress_fields(self):
        """Test creating a fitness progress
        record with specific fields."""
        fitness_progress = FitnessProgress.objects.create(
            user=self.user,
            date=date(2022, 2, 1),
            weight=Decimal('178.00'),
            goal_weight=Decimal('155.00'),
            achieved_goals='Completed first half-marathon',
            notes='Need to improve hydration next time.'
        )
        self.assertEqual(fitness_progress.user, self.user)
        self.assertEqual(fitness_progress.date, date(2022, 2, 1))
        self.assertEqual(fitness_progress.weight, Decimal('178.00'))
        self.assertEqual(fitness_progress.goal_weight, Decimal('155.00'))
        self.assertEqual(fitness_progress.achieved_goals,
                         'Completed first half-marathon')
        self.assertEqual(fitness_progress.notes,
                         'Need to improve hydration next time.')

    def test_fitness_progress_unique_user_date(self):
        """Test that FitnessProgress enforces
         unique user and date combinations."""
        FitnessProgress.objects.create(
            user=self.user,
            date=date(2022, 3, 1),
            weight=Decimal('175.00')
        )
        with self.assertRaises(IntegrityError):
            FitnessProgress.objects.create(
                user=self.user,
                date=date(2022, 3, 1),
                weight=Decimal('174.00')
            )
