from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty")
        return value

    def validate_mobile_number(self, value):
        if len(value) != 10 or not value.isdigit():
            raise serializers.ValidationError("Mobile number must be 10 digits")
        return value

    class Meta:
        model = Contact
        fields = "__all__"
