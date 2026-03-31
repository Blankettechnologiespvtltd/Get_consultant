from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty")
        return value

    def validate_mobile(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Mobile must contain only numbers")
        if len(value) != 10:
            raise serializers.ValidationError("Mobile must be exactly 10 digits")
        return value

    class Meta:
        model = Contact
        fields = "__all__"
