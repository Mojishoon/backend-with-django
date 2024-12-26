from rest_framework import serializers

from .models import SelectedExam

from users.models import User

from examschedules.models import ExamSchedule

class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role', 'date_of_birth', 'is_superuser', 'is_staff']

class SimpleExamScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExamSchedule
        fields = ['id', 'exam', 'start_date']


class SimpleStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class SelectedExamSerializer(serializers.ModelSerializer):
    exam_schedule_id = serializers.IntegerField(write_only=True)
    exam_schedule = SimpleExamScheduleSerializer('exam_schedule_id' , many=False, read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    student = SimpleStudentSerializer('student_id', many=False, read_only=True)
    recorder_id = serializers.IntegerField(write_only=True, required=False)
    recorder = SimpleUserSerializer('recorder_id' , many=False, read_only=True)

    class Meta:
        model = SelectedExam
        fields = ['id', 'grade', 'is_participated', 'student', 'exam_schedule_id', 'exam_schedule', 'student_id',
                  'recorder', 'recorder_id', 'record_date']


class SelectedExamUpdateSerializer(SelectedExamSerializer):
    exam_schedule_id = serializers.IntegerField(write_only=True, required=False)
    student_id = serializers.IntegerField(write_only=True, required=False)


class SelectedExamRequestSerializer(SelectedExamSerializer):

    class Meta:
        model = SelectedExam
        fields = ['grade', 'is_participated', 'student_id', 'exam_schedule_id']