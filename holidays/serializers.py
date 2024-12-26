from rest_framework import serializers

from .models import Holiday

from users.models import User


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role', 'date_of_birth', 'is_superuser', 'is_staff']

class HolidaySerializer(serializers.ModelSerializer):
    recorder_id = serializers.IntegerField(required=False, write_only=True)
    recorder = SimpleUserSerializer('recorder_id' , many=False, read_only=True)

    class Meta:
        model = Holiday
        fields = ['id', 'holiday_date', 'record_date', 'recorder', 'recorder_id']


class HolidayRequestSerializer(HolidaySerializer):

    class Meta:
        model = Holiday
        fields = ['holiday_date']
