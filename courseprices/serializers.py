from rest_framework import serializers

from .models import CoursePrice

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


class CoursePriceSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(write_only=True)
    course = SimpleCourseSerializer('course_id' , many=False, read_only=True)
    recorder_id = serializers.IntegerField(write_only=True, required=False)
    recorder = SimpleUserSerializer('recorder_id' , many=False, read_only=True)

    class Meta:
        model = CoursePrice
        fields = ['id', 'public_price', 'private_price', 'date', 'duration', 'record_date', 'course_id', 'course',
                  'recorder', 'recorder_id']


class CoursePriceUpdateSerializer(CoursePriceSerializer):
    course_id = serializers.IntegerField(write_only=True, required=False)


class CoursePriceRequestSerializer(CoursePriceSerializer):

    class Meta:
        model = CoursePrice
        fields = ['public_price', 'private_price', 'date', 'duration', 'course_id',]