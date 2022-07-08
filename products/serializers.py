from accounts.serializers import ProductDisplayWithSellerSerializer
from rest_framework import serializers
from .models import Product

class CreateProductSerializer(serializers.ModelSerializer):
    seller = ProductDisplayWithSellerSerializer(read_only=True)
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["seller", "id"]

class ListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["id"]

