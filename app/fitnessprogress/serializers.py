"""
Serializers for fitnessprogress APIs
"""

from rest_framework import serializers
from core.models import FitnessProgress


class FitnessProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessProgress
        fields = '__all__'
        read_only_fields = ('user',)
