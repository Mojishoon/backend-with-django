from datetime import datetime

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Classroom

from .serializers import ClassroomSerializer, ClassroomUpdateSerializer, ClassroomRequestSerializer

from institutemanager.dependencies import pagination, authorization

from django.db.models import Q

from django.db import IntegrityError

from inspect import currentframe


class ClassroomList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[OpenApiParameter('search'), OpenApiParameter('size'), OpenApiParameter('page'),
                               OpenApiParameter('building'), OpenApiParameter('lesson_group')])
    def get(self, request):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            size = request.query_params.get('size', 20)
            page = request.query_params.get('page', 1)
            search = request.query_params.get('search')
            building = request.query_params.get('building')
            lesson_group = request.query_params.get('lesson_group')
            criteria = ((Q(name__contains=search) if search else Q()) &
                        (Q(building=building) if building else Q()) &
                        (Q(lesson_group=lesson_group) if lesson_group else Q()))
            paginated_classroom = pagination(Classroom, size, page, criteria)
            serializer = ClassroomSerializer(paginated_classroom, many=True)
            return Response(serializer.data + [{"size": size, "page": page}])


    @extend_schema(request=ClassroomRequestSerializer)
    def post(self, request):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
                request.data["recorder_id"] = request.user.id
                serializer = ClassroomSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError as e:
                return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)



class ClassroomDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                classroom = Classroom.objects.get(pk=pk)
                serializer = ClassroomSerializer(classroom)
                return Response(serializer.data)
            except Classroom.DoesNotExist:
                return Response({"error": "classroom not found"} ,status=status.HTTP_404_NOT_FOUND)


    @extend_schema(request=ClassroomRequestSerializer)
    def put(self, request, pk):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
                request.data["recorder_id"] = request.user.id
                classroom = Classroom.objects.get(pk=pk)
                classroom_data = ClassroomUpdateSerializer(classroom).data
                classroom_data.update(request.data)
                serializer = ClassroomUpdateSerializer(classroom, data=classroom_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Classroom.DoesNotExist:
                return Response({"error": "classroom not found"}, status=status.HTTP_404_NOT_FOUND)
            except IntegrityError as e:
                return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                classroom = Classroom.objects.get(pk=pk)
                classroom.delete()
                return Response({"massage": "classroom deleted"}, status=status.HTTP_202_ACCEPTED)
            except Classroom.DoesNotExist:
                return Response({"error": "classroom not found"}, status=status.HTTP_404_NOT_FOUND)
            except IntegrityError as e:
                return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)