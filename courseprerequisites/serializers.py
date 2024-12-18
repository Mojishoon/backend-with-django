from rest_framework import serializers

from .models import CoursePrerequisite

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


class CoursePrerequisiteSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(write_only=True)
    course = SimpleCourseSerializer('course_id' , many=False, read_only=True)
    prerequisite_id = serializers.IntegerField(write_only=True)
    prerequisite = SimpleCourseSerializer('prerequisite_id', many=False, read_only=True)
    recorder_id = serializers.IntegerField(write_only=True, required=False)
    recorder = SimpleUserSerializer('recorder_id' , many=False, read_only=True)

    class Meta:
        model = CoursePrerequisite
        fields = ['course', 'prerequisite', 'course_id', 'prerequisite_id', 'recorder', 'recorder_id', 'record_date']


class CoursePrerequisiteUpdateSerializer(CoursePrerequisiteSerializer):
    course_id = serializers.IntegerField(write_only=True, required=False)
    prerequisite_id = serializers.IntegerField(write_only=True, required=False)