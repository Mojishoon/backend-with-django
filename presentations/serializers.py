from rest_framework import serializers

from .models import Presentation

from users.models import User

from courses.models import Course

class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'first_name', 'last_name', 'father_name', 'gender', 'role', 'date_of_birth',
                  'national_code', 'recruitment_date', 'is_superuser', 'is_staff', 'is_active', 'record_date',
                  'recorder', 'last_login']

class SimpleCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'name', 'record_date', 'lesson', 'recorder']


class SimpleTeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class PresentationSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(write_only=True)
    course = SimpleCourseSerializer('course_id' , many=False, read_only=True)
    teacher_id = serializers.IntegerField(write_only=True)
    teacher = SimpleTeacherSerializer('teacher_id', many=False, read_only=True)
    recorder_id = serializers.IntegerField(write_only=True, required=False)
    recorder = SimpleUserSerializer('recorder_id' , many=False, read_only=True)

    class Meta:
        model = Presentation
        fields = ['id', 'is_private', 'session_count', 'start_date', 'end_date', 'course', 'teacher', 'course_id',
                  'teacher_id', 'recorder', 'recorder_id', 'record_date']


class PresentationUpdateSerializer(PresentationSerializer):
    course_id = serializers.IntegerField(write_only=True, required=False)
    teacher_id = serializers.IntegerField(write_only=True, required=False)