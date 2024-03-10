"""
Serializers for fitness APIs
"""
from rest_framework import serializers
from core.models import Exercise, MuscleGroup


class MuscleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuscleGroup
        fields = ['id', 'name', 'description']


class ExerciseSerializer(serializers.ModelSerializer):
    target_muscles = serializers.PrimaryKeyRelatedField(
        many=True, queryset=MuscleGroup.objects.all()
    )

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description',
                  'instructions', 'target_muscles']

    def create(self, validated_data):
        target_muscles_data = validated_data.pop('target_muscles')
        exercise = Exercise.objects.create(**validated_data)
        exercise.target_muscles.set(target_muscles_data)
        return exercise
