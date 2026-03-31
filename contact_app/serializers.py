from rest_framework import serializers
from .models import Contact
from rest_framework.validators import UniqueValidator

class ContactSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=Contact.objects.all(),
                message="Email already exists"
            )
        ]
    )

    mobile = serializers.CharField(
        max_length=10,
        validators=[
            UniqueValidator(
                queryset=Contact.objects.all(),
                message="Mobile number already exists"
            )
        ]
    )

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty")
        return value.strip()   # ✅ trims spaces (small upgrade)

    def validate_mobile(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Mobile must contain only numbers")
        if len(value) != 10:
            raise serializers.ValidationError("Mobile must be exactly 10 digits")
        return value

    class Meta:
        model = Contact
        fields = "__all__"