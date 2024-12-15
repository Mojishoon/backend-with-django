from rest_framework import serializers

from .models import Course

from users.models import User

from lessons.models import Lesson

class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'first_name', 'last_name', 'father_name', 'gender', 'role', 'date_of_birth',
                  'national_code', 'recruitment_date', 'is_superuser', 'is_staff', 'is_active', 'record_date',
                  'recorder', 'last_login']

class SimpleLessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'record_date', 'lesson_group', 'recorder']


class CourseSerializer(serializers.ModelSerializer):
    lesson = SimpleLessonSerializer(many=False, read_only=True)
    recorder = SimpleUserSerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'record_date', 'lesson', 'recorder']
