from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Exam

from .serializers import ExamSerializer, ExamUpdateSerializer

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class ExamList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        course = request.query_params.get('course')
        if course:
            criteria = (Q(course=course))
        else:
            criteria = Q()
        paginated_exam = pagination(Exam, size, page, criteria)
        serializer = ExamSerializer(paginated_exam, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])

    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            serializer = ExamSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)



class ExamDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            exam = Exam.objects.get(pk=pk)
            serializer = ExamSerializer(exam)
            return Response(serializer.data)
        except Exam.DoesNotExist:
            return Response({"error": "exam not found"} ,status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            exam = Exam.objects.get(pk=pk)
            exam_data = ExamUpdateSerializer(exam).data
            exam_data.update(request.data)
            serializer = ExamUpdateSerializer(exam, data=exam_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exam.DoesNotExist:
            return Response({"error": "exam not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            exam = Exam.objects.get(pk=pk)
            exam.delete()
            return Response({"massage": "exam deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Exam.DoesNotExist:
            return Response({"error": "exam not found"}, status=status.HTTP_404_NOT_FOUND)