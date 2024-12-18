from rest_framework import serializers

from .models import Classroom

from users.models import User

from lessongroups.models import LessonGroup

from buildings.models import Building

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


class SimpleBuildingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = ['id', 'name', 'location', 'record_date', 'recorder']


class ClassroomSerializer(serializers.ModelSerializer):
    building_id = serializers.IntegerField(write_only=True)
    building = SimpleBuildingSerializer('building_id', many=False, read_only=True)
    lesson_group_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    lesson_group = SimpleLessonGroupSerializer('lesson_group_id' , many=False, read_only=True)
    recorder_id = serializers.IntegerField(write_only=True, required=False)
    recorder = SimpleUserSerializer('recorder_id' , many=False, read_only=True)

    class Meta:
        model = Classroom
        fields = ['id', 'name', 'record_date', 'capacity', 'floor', 'lesson_group', 'recorder', 'lesson_group_id',
                  'recorder_id', 'building', 'building_id']

class ClassroomUpdateSerializer(ClassroomSerializer):
    building_id = serializers.IntegerField(write_only=True, required=False)
