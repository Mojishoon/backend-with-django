from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Course

from lessons.models import Lesson

from users.models import User

from .serializers import CourseSerializer

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class CourseList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        q = request.query_params.get('q')
        lesson = request.query_params.get('lesson')
        if q or lesson:
            criteria = (Q(name__contains=q) &
                        Q(lesson=q))
        else:
            criteria = Q()
        paginated_lesson = pagination(Course, size, page, criteria)
        serializer = CourseSerializer(paginated_lesson, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])

    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            serializer = CourseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data["lesson"] = Lesson.objects.get(pk=request.data["lesson"])
                serializer.validated_data["recorder"] = User.objects.get(pk=request.user.id)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)



class CourseDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            serializer = CourseSerializer(course)
            return Response(serializer.data)
        except Course.DoesNotExist:
            return Response({"error": "course not found"} ,status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            course = Course.objects.get(pk=pk)
            course_data = CourseSerializer(course).data
            course_data.update(request.data)
            serializer = CourseSerializer(course, data=course_data)
            if serializer.is_valid():
                if "lesson" in request.data:
                    serializer.validated_data["lesson"] = Lesson.objects.get(pk=course_data["lesson"])
                else:
                    serializer.validated_data["lesson"] = Lesson.objects.get(
                        pk=course_data["lesson"]["id"])
                serializer.validated_data["recorder"] = User.objects.get(pk=request.user.id)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Lesson.DoesNotExist:
            return Response({"error": "course not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            course.delete()
            return Response({"massage": "course deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Lesson.DoesNotExist:
            return Response({"error": "course not found"}, status=status.HTTP_404_NOT_FOUND)
