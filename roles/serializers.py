from rest_framework import serializers

from .models import Role

from users.models import User

class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role', 'date_of_birth', 'is_superuser', 'is_staff']

class RoleSerializer(serializers.ModelSerializer):
    recorder_id = serializers.IntegerField(required=False, write_only=True)
    recorder = SimpleUserSerializer('recorder_id' , many=False, read_only=True)

    class Meta:
        model = Role
        fields = ['id', 'name', 'record_date', 'recorder', 'recorder_id']


class RoleRequestSerializer(RoleSerializer):

    class Meta:
        model = Role
        fields = ['name']