from rest_framework import serializers

from .models import LessonGroup

from users.models import User


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'first_name', 'last_name', 'father_name', 'gender', 'role', 'date_of_birth',
                  'national_code', 'recruitment_date', 'is_superuser', 'is_staff', 'is_active', 'record_date',
                  'recorder', 'last_login']

class LessonGroupSerializer(serializers.ModelSerializer):
    recorder = SimpleUserSerializer(many=False, read_only=True)

    class Meta:
        model = LessonGroup
        fields = ['id', 'name', 'record_date', 'recorder']
