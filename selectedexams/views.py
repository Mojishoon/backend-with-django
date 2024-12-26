from datetime import datetime

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import SelectedExam

from .serializers import SelectedExamSerializer, SelectedExamUpdateSerializer, SelectedExamRequestSerializer

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class SelectedExamList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[OpenApiParameter('page'), OpenApiParameter('size'), OpenApiParameter('student'),
                               OpenApiParameter('exam_schedule')])
    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        exam_schedule = request.query_params.get('exam')
        student = request.query_params.get('student')
        criteria = ((Q(student=student) if student else Q()) &
                    (Q(exam_schedule=exam_schedule) if exam_schedule else Q()))
        paginated_selected_exam = pagination(SelectedExam, size, page, criteria)
        serializer = SelectedExamSerializer(paginated_selected_exam, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])


    @extend_schema(request=SelectedExamRequestSerializer)
    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            serializer = SelectedExamSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)


class SelectedExamDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            selected_exam = SelectedExam.objects.get(pk=pk)
            serializer = SelectedExamSerializer(selected_exam)
            return Response(serializer.data)
        except SelectedExam.DoesNotExist:
            return Response({"error": "selected exam not found"} ,status=status.HTTP_404_NOT_FOUND)


    @extend_schema(request=SelectedExamRequestSerializer)
    def put(self, request, pk):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            selected_exam = SelectedExam.objects.get(pk=pk)
            selected_exam_data = SelectedExamUpdateSerializer(selected_exam).data
            selected_exam_data.update(request.data)
            serializer = SelectedExamUpdateSerializer(selected_exam, data=selected_exam_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SelectedExam.DoesNotExist:
            return Response({"error": "selected exam not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            selected_exam = SelectedExam.objects.get(pk=pk)
            selected_exam.delete()
            return Response({"massage": "selected exam deleted"}, status=status.HTTP_202_ACCEPTED)
        except SelectedExam.DoesNotExist:
            return Response({"error": "selected exam not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)
