from rest_framework import serializers

from .models import Exam

from users.models import User

from courses.models import Course

class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role', 'date_of_birth', 'is_superuser', 'is_staff']

class SimpleCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'name', 'lesson']


class ExamSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(write_only=True)
    course = SimpleCourseSerializer('course_id' , many=False, read_only=True)
    recorder_id = serializers.IntegerField(write_only=True, required=False)
    recorder = SimpleUserSerializer('recorder_id' , many=False, read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'price', 'course_id', 'course', 'record_date', 'recorder', 'recorder_id']


class ExamUpdateSerializer(ExamSerializer):
    course_id = serializers.IntegerField(write_only=True, required=False)