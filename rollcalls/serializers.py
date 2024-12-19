from rest_framework import serializers

from .models import RollCall

from users.models import User

from presentationsessions.models import PresentationSession

class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role', 'date_of_birth', 'is_superuser', 'is_staff']


class SimpleStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class SimplePresentationSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PresentationSession
        fields = ['id', 'start_time', 'end_time', 'is_cancelled', 'is_extra', 'presentation', 'classroom']


class RollCallSerializer(serializers.ModelSerializer):
    presentation_session_id = serializers.IntegerField(write_only=True)
    presentation_session = SimplePresentationSessionSerializer(
        'presentation_session_id' , many=False, read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    student = SimpleStudentSerializer('student_id', many=False, read_only=True)
    recorder_id = serializers.IntegerField(write_only=True, required=False)
    recorder = SimpleUserSerializer('recorder_id' , many=False, read_only=True)

    class Meta:
        model = RollCall
        fields = ['id', 'is_present', 'delay', 'comment', 'presentation_session', 'student', 'student_id', 'recorder',
                  'recorder_id', 'record_date', 'presentation_session_id']


class RollCallUpdateSerializer(RollCallSerializer):
    presentation_session_id = serializers.IntegerField(write_only=True, required=False)
    student_id = serializers.IntegerField(write_only=True, required=False)