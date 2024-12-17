from rest_framework import serializers

from django.core import validators

from roles.models import Role

from .models import User

class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'first_name', 'last_name', 'father_name', 'gender', 'role', 'date_of_birth',
                  'national_code', 'recruitment_date', 'is_superuser', 'is_staff', 'is_active', 'record_date', 'recorder',
                  'last_login']

class SimpleRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[validators.RegexValidator(
        regex=r'^989[0-3,9]\d{8}$', message="Phone number must be entered in the format: '989-3-9'."
    )])
    password = serializers.CharField(write_only=True)
    role_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    recorder_id = serializers.IntegerField(required=False, write_only=True)
    role = SimpleRoleSerializer('role_id', read_only=True)
    recorder = SimpleUserSerializer('recorder_id', many=False, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'first_name', 'last_name', 'father_name', 'gender', 'role', 'date_of_birth',
                  'national_code', 'recruitment_date', 'is_superuser', 'is_staff', 'is_active', 'record_date','last_login',
                  'password', 'recorder', 'recorder_id', 'role_id']
