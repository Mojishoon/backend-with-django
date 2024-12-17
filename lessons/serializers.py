from rest_framework import serializers

from .models import Lesson

from users.models import User

from lessongroups.models import LessonGroup

class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'first_name', 'last_name', 'father_name', 'gender', 'role', 'date_of_birth',
                  'national_code', 'recruitment_date', 'is_superuser', 'is_staff', 'is_active', 'record_date',
                  'recorder', 'last_login']

class SimpleLessonGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonGroup
        fields = ['id', 'name', 'record_date', 'recorder']


class LessonSerializer(serializers.ModelSerializer):
    lesson_group_id = serializers.IntegerField(write_only=True)
    lesson_group = SimpleLessonGroupSerializer('lesson_group_id' , many=False, read_only=True)
    recorder_id = serializers.IntegerField(write_only=True, required=False)
    recorder = SimpleUserSerializer('recorder_id' , many=False, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'record_date', 'lesson_group', 'recorder', 'lesson_group_id', 'recorder_id']

class LessonUpdateSerializer(LessonSerializer):
    lesson_group_id = serializers.IntegerField(write_only=True, required=False)
