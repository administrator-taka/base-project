from rest_framework import serializers

from .models import Test


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test  # このシリアライザがTestモデルを使用することを指定します
        fields = '__all__'  # Testモデルのすべてのフィールドを含めることを指定します
