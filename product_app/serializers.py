from product_app.models import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__" # We serialize all the fields we have
        