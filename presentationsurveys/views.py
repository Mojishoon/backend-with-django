from datetime import datetime

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import PresentationSurvey

from .serializers import (PresentationSurveySerializer, PresentationSurveyUpdateSerializer,
                          PresentationSurveyRequestSerializer)

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class PresentationSurveyList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[OpenApiParameter('size'), OpenApiParameter('page'), OpenApiParameter('presentation'),
                               OpenApiParameter('student'), OpenApiParameter('survey_category')])
    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        presentation = request.query_params.get('presentation')
        student = request.query_params.get('student')
        survey_category = request.query_params.get('survey_category')
        criteria = ((Q(student=student) if student else Q()) &
                    (Q(presentation=presentation) if presentation else Q()) &
                    (Q(survey_category=survey_category) if survey_category else Q()))
        paginated_presentation_survey = pagination(PresentationSurvey, size, page, criteria)
        serializer = PresentationSurveySerializer(paginated_presentation_survey, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])


    @extend_schema(request=PresentationSurveyRequestSerializer)
    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            serializer = PresentationSurveySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)


class PresentationSurveyDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            presentation_survey = PresentationSurvey.objects.get(pk=pk)
            serializer = PresentationSurveySerializer(presentation_survey)
            return Response(serializer.data)
        except PresentationSurvey.DoesNotExist:
            return Response({"error": "presentation survey not found"} ,status=status.HTTP_404_NOT_FOUND)


    @extend_schema(request=PresentationSurveyRequestSerializer)
    def put(self, request, pk):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            presentation_survey = PresentationSurvey.objects.get(pk=pk)
            presentation_survey_data = PresentationSurveyUpdateSerializer(presentation_survey).data
            presentation_survey_data.update(request.data)
            serializer = PresentationSurveyUpdateSerializer(presentation_survey, data=presentation_survey_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PresentationSurvey.DoesNotExist:
            return Response({"error": "presentation survey not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            presentation_survey = PresentationSurvey.objects.get(pk=pk)
            presentation_survey.delete()
            return Response({"massage": "presentation survey deleted"}, status=status.HTTP_202_ACCEPTED)
        except PresentationSurvey.DoesNotExist:
            return Response({"error": "presentation survey not found"}, status=status.HTTP_404_NOT_FOUND)
