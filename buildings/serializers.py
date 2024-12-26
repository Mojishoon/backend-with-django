from rest_framework import serializers

from .models import Building

from users.models import User


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role', 'date_of_birth', 'is_superuser', 'is_staff']

class BuildingSerializer(serializers.ModelSerializer):
    recorder_id = serializers.IntegerField(required=False, write_only=True)
    recorder = SimpleUserSerializer('recorder_id' , many=False, read_only=True)

    class Meta:
        model = Building
        fields = ['id', 'name', 'location', 'recorder', 'recorder_id', 'record_date']

class BuildingRequestSerializer(serializers.ModelSerializer):

     class Meta:
         model = Building
         fields = ['name', 'location']
