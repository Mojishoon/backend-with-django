from rest_framework import serializers

from .models import PresentationSurvey

from users.models import User

from surveycategories.models import SurveyCategory

from presentations.models import Presentation

class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role', 'date_of_birth', 'is_superuser', 'is_staff']

class SimplePresentationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Presentation
        fields = ['id', 'course', 'teacher', 'is_private', 'start_date', 'end_date']


class SimpleSurveyCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SurveyCategory
        fields = ['id', 'name']


class SimpleStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class PresentationSurveySerializer(serializers.ModelSerializer):
    presentation_id = serializers.IntegerField(write_only=True)
    presentation = SimplePresentationSerializer('presentation_id' , many=False, read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    student = SimpleStudentSerializer('student_id', many=False, read_only=True)
    survey_category_id = serializers.IntegerField(write_only=True)
    survey_category = SimpleSurveyCategorySerializer('survey_category_id', many=False, read_only=True)
    recorder_id = serializers.IntegerField(write_only=True, required=False)
    recorder = SimpleUserSerializer('recorder_id' , many=False, read_only=True)

    class Meta:
        model = PresentationSurvey
        fields = ['id', 'score', 'student', 'presentation_id', 'presentation', 'student_id', 'survey_category',
                  'survey_category_id', 'recorder', 'recorder_id', 'record_date']


class PresentationSurveyUpdateSerializer(PresentationSurveySerializer):
    presentation_id = serializers.IntegerField(write_only=True, required=False)
    student_id = serializers.IntegerField(write_only=True, required=False)
    survey_category_id = serializers.IntegerField(write_only=True, required=False)