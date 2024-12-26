from rest_framework import serializers

from .models import PermissionGroup

from users.models import User


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role', 'date_of_birth', 'is_superuser', 'is_staff']

class PermissionGroupSerializer(serializers.ModelSerializer):
    recorder_id = serializers.IntegerField(required=False, write_only=True)
    recorder = SimpleUserSerializer('recorder_id' , many=False, read_only=True)

    class Meta:
        model = PermissionGroup
        fields = ['id', 'name', 'record_date', 'recorder', 'recorder_id']


class PermissionGroupRequestSerializer(PermissionGroupSerializer):

    class Meta:
        model = PermissionGroup
        fields = ['name']
