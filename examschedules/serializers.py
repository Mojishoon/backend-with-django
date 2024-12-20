from rest_framework import serializers

from .models import ExamSchedule

from users.models import User

from exams.models import Exam

class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role', 'date_of_birth', 'is_superuser', 'is_staff']

class SimpleExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exam
        fields = ['id', 'course', 'price']


class ExamScheduleSerializer(serializers.ModelSerializer):
    exam_id = serializers.IntegerField(write_only=True)
    exam = SimpleExamSerializer('exam_id' , many=False, read_only=True)
    recorder_id = serializers.IntegerField(write_only=True, required=False)
    recorder = SimpleUserSerializer('recorder_id' , many=False, read_only=True)

    class Meta:
        model = ExamSchedule
        fields = ['id', 'start_date', 'exam', 'exam_id', 'record_date', 'recorder', 'recorder_id']


class ExamScheduleUpdateSerializer(ExamScheduleSerializer):
    exam_id = serializers.IntegerField(write_only=True, required=False)