from rest_framework import serializers

from .models import FinancialTransaction

from users.models import User

from financialcategories.models import FinancialCategory

from presentations.models import Presentation

from selectedpresentations.models import SelectedPresentation

from selectedexams.models import SelectedExam

from paycategories.models import PayCategory


class SimpleRecorderSerializer(serializers.Serializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role', 'date_of_birth', 'is_superuser', 'is_staff']


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role']

class SimpleFinancialCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FinancialCategory
        fields = ['id', 'name']

class SimplePresentationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Presentation
        fields = ['id', 'course', 'teacher', 'is_private']


class SimpleSelectedPresentationSerializer(serializers.ModelSerializer):

    class Meta:
        model = SelectedPresentation
        fields = ['id', 'presentation', 'student']


class SimpleSelectedExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = SelectedExam
        fields = ['id', 'exam_schedule', 'student', 'is_participated']


class SimplePayCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PayCategory
        fields = ['id', 'name']


class FinancialTransactionSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    user = SimpleUserSerializer('lesson_group_id' , many=False, read_only=True)
    financial_category_id = serializers.IntegerField(write_only=True)
    financial_category = SimpleFinancialCategorySerializer('financial_category' , many=False, read_only=True)
    presentation_id = serializers.IntegerField(write_only=True, allow_null=True)
    presentation = SimplePresentationSerializer('presentation' , many=False, read_only=True)
    selected_presentation_id = serializers.IntegerField(write_only=True, allow_null=True)
    selected_presentation = SimpleSelectedPresentationSerializer('selected_presentation', many=False,
                                                                 read_only=True)
    selected_exam_id = serializers.IntegerField(write_only=True, allow_null=True)
    selected_exam = SimpleSelectedExamSerializer('selected_exam', many=False, read_only=True)
    pay_category_id = serializers.IntegerField(write_only=True)
    pay_category = SimplePayCategorySerializer('pay_category', many=False, read_only=True)
    recorder_id = serializers.IntegerField(write_only=True, required=False)
    recorder = SimpleUserSerializer('recorder_id' , many=False, read_only=True)

    class Meta:
        model = FinancialTransaction
        fields = ['id', 'amount', 'transaction_date', 'pay_reference', 'user', 'user_id', 'financial_category',
                  'financial_category_id', 'presentation_id', 'presentation', 'selected_presentation',
                  'selected_presentation_id', 'selected_exam', 'selected_exam_id', 'pay_category', 'pay_category_id',
                  'record_date', 'recorder', 'recorder_id']

class FinancialTransactionUpdateSerializer(FinancialTransactionSerializer):
    user_id = serializers.IntegerField(write_only=True, required=False)
    financial_category_id = serializers.IntegerField(write_only=True, required=False)
    presentation_id = serializers.IntegerField(write_only=True, required=False)
    selected_presentation_id = serializers.IntegerField(write_only=True, required=False)
    selected_exam_id = serializers.IntegerField(write_only=True, required=False)
    pay_category_id = serializers.IntegerField(write_only=True, required=False)

