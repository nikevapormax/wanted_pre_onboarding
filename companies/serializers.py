from pyexpat import model
from rest_framework import serializers

from .models import Recruitments as RecruitmentsModel


class RecruitmentsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RecruitmentsModel
        fields = ["company", "position", "recruit_compensation", "contents", "skill"]
    
