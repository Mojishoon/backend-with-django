from rest_framework import serializers

from .models import PermissionGroupDefine

from users.models import User

from permissions.models import Permission

from permissiongroups.models import PermissionGroup

class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role', 'date_of_birth', 'is_superuser', 'is_staff']

class SimplePermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ['id', 'name', 'parent']


class SimplePermissionGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = PermissionGroup
        fields = ['id', 'name']


class PermissionGroupDefineSerializer(serializers.ModelSerializer):
    permission_id = serializers.IntegerField(write_only=True)
    permission = SimplePermissionSerializer('permission_id' , many=False, read_only=True)
    permission_group_id = serializers.IntegerField(write_only=True)
    permission_group = SimplePermissionGroupSerializer('permission_group_id', many=False, read_only=True)
    recorder_id = serializers.IntegerField(write_only=True, required=False)
    recorder = SimpleUserSerializer('recorder_id' , many=False, read_only=True)

    class Meta:
        model = PermissionGroupDefine
        fields = ['id', 'permission', 'permission_id', 'permission_group', 'permission_group_id', 'recorder',
                  'recorder_id', 'record_date']


class PermissionGroupDefineUpdateSerializer(PermissionGroupDefineSerializer):
    permission_id = serializers.IntegerField(write_only=True, required=False)
    permission_group_id = serializers.IntegerField(write_only=True, required=False)