"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email),
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'


class MuscleGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    instructions = models.TextField()
    target_muscles = models.ManyToManyField(
        MuscleGroup, related_name='exercises')

    def __str__(self):
        return self.name


class WorkoutPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='workout_plans')
    title = models.CharField(max_length=255)
    frequency = models.IntegerField(
        help_text='Number of workouts per week')
    goal = models.TextField(blank=True, null=True)
    session_duration = \
        models.IntegerField(help_text='Duration of each workout'
                                      ' session in minutes')

    def __str__(self):
        return f"{self.title} - {self.user.email}"


class WorkoutExercise(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan,
                                     related_name='workout_exercises',
                                     on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField(default=0)
    repetitions = models.IntegerField(default=0)
    duration = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.exercise.name} -" \
               f" {self.sets} sets of {self.repetitions}"
