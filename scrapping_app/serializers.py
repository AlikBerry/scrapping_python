from rest_framework import serializers
from .models import *

class DataInfo(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ["name","size","url","color"]

class ProductItemsSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = ["field","value","tag_name"]


class ProductSerializers(serializers.ModelSerializer):
    product_tags = ProductItemsSerializers(many=True)

    class Meta:
        model = ProductTag
        fields = ["name", "product_tags"]