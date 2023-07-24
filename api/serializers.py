from rest_framework import serializers
from .models import Product, SavedItem
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class SavedItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = SavedItem
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')