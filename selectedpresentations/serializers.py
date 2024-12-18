from rest_framework import serializers

from .models import SelectedPresentation

from users.models import User

from presentations.models import Presentation

class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role', 'date_of_birth', 'is_superuser', 'is_staff']

class SimplePresentationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Presentation
        fields = ['id', 'course', 'teacher', 'is_private', 'start_date', 'end_date']


class SimpleStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class SelectedPresentationSerializer(serializers.ModelSerializer):
    presentation_id = serializers.IntegerField(write_only=True)
    presentation = SimplePresentationSerializer('presentation_id' , many=False, read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    student = SimpleStudentSerializer('student_id', many=False, read_only=True)
    recorder_id = serializers.IntegerField(write_only=True, required=False)
    recorder = SimpleUserSerializer('recorder_id' , many=False, read_only=True)

    class Meta:
        model = SelectedPresentation
        fields = ['id', 'grade', 'student', 'presentation_id', 'presentation', 'student_id', 'recorder', 'recorder_id',
                  'record_date']


class SelectedPresentationUpdateSerializer(SelectedPresentationSerializer):
    presentation_id = serializers.IntegerField(write_only=True, required=False)
    student_id = serializers.IntegerField(write_only=True, required=False)