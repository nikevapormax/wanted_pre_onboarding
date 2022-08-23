from pyexpat import model
from rest_framework import serializers

from .models import Recruitments as RecruitmentsModel


class RecruitmentsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RecruitmentsModel
        fields = ["company", "position", "recruit_compensation", "contents", "skill"]
    

class RecruitmentsChangeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RecruitmentsModel
        fields = ["company", "position", "recruit_compensation", "contents", "skill"]
    
    def validate(self, data):
        if data.get("company"):
            data.pop("company")
        print(data)
        return data
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        
        return instance