from rest_framework import serializers

from .models import Course

from users.models import User

from lessons.models import Lesson

class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role', 'date_of_birth', 'is_superuser', 'is_staff']

class SimpleLessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ['id', 'name','lesson_group']


class CourseSerializer(serializers.ModelSerializer):
    lesson_id = serializers.IntegerField(write_only=True)
    lesson = SimpleLessonSerializer('lesson_id' , many=False, read_only=True)
    recorder_id = serializers.IntegerField(write_only=True, required=False)
    recorder = SimpleUserSerializer('recorder_id' , many=False, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'record_date', 'lesson', 'recorder', 'lesson_id', 'recorder_id']

class CourseUpdateSerializer(CourseSerializer):
    lesson_id = serializers.IntegerField(write_only=True, required=False)


class CourseRequestSerializer(CourseSerializer):

    class Meta:
        model = Course
        fields = ['name', 'lesson_id']
