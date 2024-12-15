from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Lesson

from lessongroups.models import LessonGroup

from users.models import User

from .serializers import LessonSerializer

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class LessonList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        q = request.query_params.get('q')
        lesson_group = request.query_params.get('lesson_group')
        if q or lesson_group:
            criteria = (Q(name__contains=q) &
                        Q(lessongroup=q))
        else:
            criteria = Q()
        paginated_lesson = pagination(Lesson, size, page, criteria)
        serializer = LessonSerializer(paginated_lesson, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])

    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            serializer = LessonSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data["lesson_group"] = LessonGroup.objects.get(pk=request.data["lesson_group"])
                serializer.validated_data["recorder"] = User.objects.get(pk=request.user.id)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)



class LessonDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            lesson = Lesson.objects.get(pk=pk)
            serializer = LessonSerializer(lesson)
            return Response(serializer.data)
        except Lesson.DoesNotExist:
            return Response({"error": "lesson not found"} ,status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            lesson = Lesson.objects.get(pk=pk)
            lesson_data = LessonSerializer(lesson).data
            lesson_data.update(request.data)
            serializer = LessonSerializer(lesson, data=lesson_data)
            if serializer.is_valid():
                if "lesson_group" in request.data:
                    serializer.validated_data["lesson_group"] = LessonGroup.objects.get(pk=lesson_data["lesson_group"])
                else:
                    serializer.validated_data["lesson_group"] = LessonGroup.objects.get(
                        pk=lesson_data["lesson_group"]["id"])
                serializer.validated_data["recorder"] = User.objects.get(pk=request.user.id)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Lesson.DoesNotExist:
            return Response({"error": "lesson not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            lesson_group = Lesson.objects.get(pk=pk)
            lesson_group.delete()
            return Response({"massage": "lesson deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Lesson.DoesNotExist:
            return Response({"error": "lesson not found"}, status=status.HTTP_404_NOT_FOUND)
