from pyexpat import model
from rest_framework import serializers

from .models import Recruitments as RecruitmentsModel


class RecruitmentsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RecruitmentsModel
        fields = ["company", "country", "region", "position", "recruit_compensation", "contents", "skill"]
    

class RecruitmentsChangeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RecruitmentsModel
        fields = ["company", "country", "region", "position", "recruit_compensation", "contents", "skill"]
    
    def validate(self, data):
        if data.get("company"):
            data.pop("company")

        return data
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        
        return instance
    

class RecruitmentsLookupSeriailizer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    
    def get_company_name(self, obj):
        return obj.company.company_name
    
    class Meta:
        model = RecruitmentsModel
        fields = ["id", "company_name", "country", "region", "position", "recruit_compensation", "skill"]