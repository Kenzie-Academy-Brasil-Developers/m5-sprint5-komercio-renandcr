from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="email already exists")])

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "is_seller", "password", "date_joined"]
        read_only_fields = ["date_joined"]
        extra_kwargs = {
            "password": {'write_only': True}, 
            
        }
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
            if key == "password":
                instance.set_password(validated_data["password"])

        instance.save()

        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class ActivateOrDeactivateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "is_seller", "date_joined","is_active"]
        read_only_fields = ["id", "email", "first_name", "last_name", "is_seller", "date_joined"]

class ProductDisplayWithSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "is_seller", "date_joined"]  
