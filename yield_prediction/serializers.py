from rest_framework import serializers
from .models import CropData


class CropDataSerializer(serializers.ModelSerializer):
    crop_yield = serializers.ReadOnlyField()

    class Meta:
        model = CropData
        fields = "__all__"
