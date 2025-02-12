from datetime import datetime

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Presentation

from .serializers import PresentationSerializer, PresentationUpdateSerializer, PresentationRequestSerializer

from institutemanager.dependencies import pagination, authorization

from django.db.models import Q

from django.db import IntegrityError

from inspect import currentframe

class PresentationList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[OpenApiParameter('page'), OpenApiParameter('size'), OpenApiParameter('course'),
                               OpenApiParameter('from_date', datetime), OpenApiParameter('to_date', datetime),
                               OpenApiParameter('is_private', bool)])
    def get(self, request):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            size = request.query_params.get('size', 20)
            page = request.query_params.get('page', 1)
            course = request.query_params.get('course')
            teacher = request.query_params.get('teacher')
            from_date = request.query_params.get('from_date')
            to_date = request.query_params.get('to_date')
            is_private = request.query_params.get('is_private')
            x = 0
            if is_private == 'false':
                is_private = False
                x += 1
            if is_private == 'true':
                is_private = True
                x += 1
            criteria = ((Q(course=course) if course else Q()) &
                        (Q(teacher=teacher) if teacher else Q()) &
                        (Q(start_date__gte=from_date) if from_date else Q()) &
                        (Q(end_date__lte=to_date) if to_date else Q()) &
                        (Q(is_private=is_private) if x else Q()))
            paginated_presentation = pagination(Presentation, size, page, criteria)
            serializer = PresentationSerializer(paginated_presentation, many=True)
            return Response(serializer.data + [{"size": size, "page": page}])

    @extend_schema(request=PresentationRequestSerializer)
    def post(self, request):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
                request.data["recorder_id"] = request.user.id
                serializer = PresentationSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError as e:
                return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)


class PresentationDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                presentation = Presentation.objects.get(pk=pk)
                serializer = PresentationSerializer(presentation)
                return Response(serializer.data)
            except Presentation.DoesNotExist:
                return Response({"error": "presentation not found"} ,status=status.HTTP_404_NOT_FOUND)

    @extend_schema(request=PresentationRequestSerializer)
    def put(self, request, pk):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
                request.data["recorder_id"] = request.user.id
                presentation = Presentation.objects.get(pk=pk)
                presentation_data = PresentationUpdateSerializer(presentation).data
                presentation_data.update(request.data)
                serializer = PresentationUpdateSerializer(presentation, data=presentation_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Presentation.DoesNotExist:
                return Response({"error": "presentation not found"}, status=status.HTTP_404_NOT_FOUND)
            except IntegrityError as e:
                return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        operation = (self.__class__.__name__ + currentframe().f_code.co_name).lower()
        if authorization(request.user, operation):
            try:
                presentation = Presentation.objects.get(pk=pk)
                presentation.delete()
                return Response({"massage": "presentation deleted"}, status=status.HTTP_202_ACCEPTED)
            except Presentation.DoesNotExist:
                return Response({"error": "presentation not found"}, status=status.HTTP_404_NOT_FOUND)
            except IntegrityError as e:
                return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)
