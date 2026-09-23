from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    user_type = serializers.CharField(source="get_user_type_display", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "full_name", "user_type", "email", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]


class UserDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "full_name",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "national_code",
            "department",
            "user_type",
            "avatar",
            "is_active",
            "is_verified",
            "created_at",
            "updated_at",
            "last_login",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "last_login"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, style={"input_type": "password"})
    password_confirm = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
            "phone_number",
            "nationa_code",
        ]

        def validate(self, data):
            if data["password"] != data["confirm_password"]:
                raise serializers.ValidationError({"password_confim": "password and confirm password are not the same"})
            return data

        def create(self, validated_data):
            validated_data.pop("password_confirm")
            password = validated_data.pop("password")
            user = User(**validated_data)
            user.set_password(password)
            user.save()
            return user
