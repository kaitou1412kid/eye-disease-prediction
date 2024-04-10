from rest_framework import serializers
from .models import CustomUser, Disease
import chardet
class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username","password","email"]
        extra_kwargs = {"password":{"write_only" : True}}
        
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class EyePredictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = ["image"]
        
    def create(self, validated_data):
        user = self.context.get('request').user
        disease, created = Disease.objects.get_or_create(user=user, defaults=validated_data)
        return disease