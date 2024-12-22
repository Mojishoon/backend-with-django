from rest_framework import serializers

from .models import Permission

class SimplePermissionSerializer(serializers.Serializer):

    class Meta:
        model = Permission
        fields = ['id', 'name']

class PermissionSerializer(serializers.ModelSerializer):
    parent = SimplePermissionSerializer()

    class Meta:
        model = Permission
        fields = ['id', 'name', 'parent']
