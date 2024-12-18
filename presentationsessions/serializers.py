from rest_framework import serializers

from .models import PresentationSession

from users.models import User

from classrooms.models import Classroom

from presentations.models import Presentation

class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role', 'date_of_birth', 'is_superuser', 'is_staff']

class SimpleClassroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classroom
        fields = ['id', 'name', 'building', 'floor']


class SimplePresentationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Presentation
        fields = ['id', 'course', 'teacher', 'is_private', 'start_date', 'end_date']


class PresentationSessionSerializer(serializers.ModelSerializer):
    presentation_id = serializers.IntegerField(write_only=True)
    presentation = SimplePresentationSerializer('presentation_id' , many=False, read_only=True)
    classroom_id = serializers.IntegerField(write_only=True)
    classroom = SimpleClassroomSerializer('classroom_id', many=False, read_only=True)
    recorder_id = serializers.IntegerField(write_only=True, required=False)
    recorder = SimpleUserSerializer('recorder_id' , many=False, read_only=True)

    class Meta:
        model = PresentationSession
        fields = ['id', 'start_time', 'end_time', 'is_cancelled', 'is_extra', 'presentation', 'classroom', 'classroom_id',
                  'recorder', 'recorder_id', 'record_date', 'presentation_id']


class PresentationSessionUpdateSerializer(PresentationSessionSerializer):
    presentation_id = serializers.IntegerField(write_only=True, required=False)
    classroom_id = serializers.IntegerField(write_only=True, required=False)