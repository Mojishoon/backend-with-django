from rest_framework import serializers

from django.contrib.auth import authenticate

from django.core import validators

from roles.models import Role

from .models import User, LoginLog

from permissiongroups.models import PermissionGroup

class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role', 'permission_group', 'date_of_birth', 'is_superuser', 'is_staff']

class SimpleRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ['id', 'name']


class SimplePermissionGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = PermissionGroup
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[validators.RegexValidator(
        regex=r'^989[0-3,9]\d{8}$', message="Phone number must be entered in the format: '989-3-9'."
    )])
    password = serializers.CharField(write_only=True)
    role_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    role = SimpleRoleSerializer('role_id', read_only=True)
    permission_group_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    permission_group = SimplePermissionGroupSerializer('permission_group_id', read_only=True)
    recorder_id = serializers.IntegerField(required=False, read_only=True)
    recorder = SimpleUserSerializer('recorder_id', many=False, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'first_name', 'last_name', 'father_name', 'gender', 'role', 'date_of_birth',
                  'national_code', 'recruitment_date', 'is_superuser', 'is_staff', 'is_active', 'record_date','last_login',
                  'password', 'permission_group', 'permission_group_id', 'recorder', 'recorder_id', 'role_id']


class UserLoginSerializer(serializers.Serializer):

    phone_number = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class LoginLogSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=False, write_only=True)
    user = SimpleUserSerializer('user_id' , many=False, read_only=True)

    class Meta:
        model = LoginLog
        fields = ['id', 'login_date', 'user', 'user_id']
