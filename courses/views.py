from datetime import datetime

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Course

from .serializers import CourseSerializer, CourseUpdateSerializer, CourseRequestSerializer

from institutemanager.dependencies import pagination, authorization

from django.db.models import Q

from django.db import IntegrityError

from inspect import currentframe

class CourseList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[OpenApiParameter('size'), OpenApiParameter('page'), OpenApiParameter('search'),
                               OpenApiParameter('lesson')])
    def get(self, request):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            size = request.query_params.get('size', 20)
            page = request.query_params.get('page', 1)
            search = request.query_params.get('search')
            lesson = request.query_params.get('lesson')
            criteria = ((Q(name__contains=search) if search else Q()) &
                        (Q(lesson=lesson) if lesson else Q()))
            paginated_course = pagination(Course, size, page, criteria)
            serializer = CourseSerializer(paginated_course, many=True)
            return Response(serializer.data + [{"size": size, "page": page}])


    @extend_schema(request=CourseRequestSerializer)
    def post(self, request):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
                request.data["recorder_id"] = request.user.id
                serializer = CourseSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError as e:
                return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)



class CourseDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                course = Course.objects.get(pk=pk)
                serializer = CourseSerializer(course)
                return Response(serializer.data)
            except Course.DoesNotExist:
                return Response({"error": "course not found"} ,status=status.HTTP_404_NOT_FOUND)


    @extend_schema(request=CourseRequestSerializer)
    def put(self, request, pk):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
                request.data["recorder_id"] = request.user.id
                course = Course.objects.get(pk=pk)
                course_data = CourseUpdateSerializer(course).data
                course_data.update(request.data)
                serializer = CourseUpdateSerializer(course, data=course_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Course.DoesNotExist:
                return Response({"error": "course not found"}, status=status.HTTP_404_NOT_FOUND)
            except IntegrityError as e:
                return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                course = Course.objects.get(pk=pk)
                course.delete()
                return Response({"massage": "course deleted"}, status=status.HTTP_202_ACCEPTED)
            except Course.DoesNotExist:
                return Response({"error": "course not found"}, status=status.HTTP_404_NOT_FOUND)
            except IntegrityError as e:
                return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)
