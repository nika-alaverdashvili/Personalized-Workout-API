"""
Serializers for the workout_plans API View.
"""
from rest_framework import serializers
from core.models import Exercise, WorkoutPlan,\
    WorkoutExercise, MuscleGroup


class MuscleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuscleGroup
        fields = ['id', 'name', 'description']


class ExerciseSerializer(serializers.ModelSerializer):
    target_muscles = MuscleGroupSerializer(many=True,
                                           read_only=True)

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description',
                  'instructions', 'target_muscles']


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.all())
    workout_plan = serializers.PrimaryKeyRelatedField(
        queryset=WorkoutPlan.objects.all(), write_only=True)

    class Meta:
        model = WorkoutExercise
        fields = ['id', 'workout_plan', 'exercise',
                  'sets', 'repetitions', 'duration']

    def create(self, validated_data):
        return WorkoutExercise.objects.create(**validated_data)


class WorkoutPlanSerializer(serializers.ModelSerializer):
    workout_exercises = WorkoutExerciseSerializer(
        many=True, read_only=True)
    create_workout_exercises = WorkoutExerciseSerializer(
        many=True, write_only=True, required=False)

    class Meta:
        model = WorkoutPlan
        fields = ['id', 'user', 'title', 'frequency', 'goal',
                  'session_duration', 'workout_exercises',
                  'create_workout_exercises']

    def create(self, validated_data):
        workout_exercises_data = validated_data.pop(
            'create_workout_exercises', [])
        workout_plan = WorkoutPlan.objects.create(**validated_data)
        for workout_exercise_data in workout_exercises_data:
            WorkoutExercise.objects.create(
                workout_plan=workout_plan, **workout_exercise_data)
        return workout_plan

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.frequency = validated_data.get(
            'frequency', instance.frequency)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.session_duration = validated_data.get(
            'session_duration', instance.session_duration)

        if 'create_workout_exercises' in validated_data:
            instance.workout_exercises.all().delete()
            for workout_exercise_data\
                    in validated_data['create_workout_exercises']:
                WorkoutExercise.objects.create(
                    workout_plan=instance, **workout_exercise_data)

        instance.save()
        return instance
