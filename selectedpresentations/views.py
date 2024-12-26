from datetime import datetime

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import SelectedPresentation

from .serializers import (SelectedPresentationSerializer, SelectedPresentationUpdateSerializer,
                          SelectedPresentationRequestSerializer)

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class SelectedPresentationList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[OpenApiParameter('page'), OpenApiParameter('size'), OpenApiParameter('student'),
                               OpenApiParameter('presentation')])
    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        presentation = request.query_params.get('presentation')
        student = request.query_params.get('student')
        criteria = ((Q(student=student) if student else Q()) &
                    (Q(presentation=presentation) if presentation else Q()))
        paginated_selected_presentation = pagination(SelectedPresentation, size, page, criteria)
        serializer = SelectedPresentationSerializer(paginated_selected_presentation, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])


    @extend_schema(request=SelectedPresentationRequestSerializer)
    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            serializer = SelectedPresentationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)


class SelectedPresentationDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            selected_presentation = SelectedPresentation.objects.get(pk=pk)
            serializer = SelectedPresentationSerializer(selected_presentation)
            return Response(serializer.data)
        except SelectedPresentation.DoesNotExist:
            return Response({"error": "selected presentation not found"} ,status=status.HTTP_404_NOT_FOUND)


    @extend_schema(request=SelectedPresentationRequestSerializer)
    def put(self, request, pk):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            selected_presentation = SelectedPresentation.objects.get(pk=pk)
            selected_presentation_data = SelectedPresentationUpdateSerializer(selected_presentation).data
            selected_presentation_data.update(request.data)
            serializer = SelectedPresentationUpdateSerializer(selected_presentation, data=selected_presentation_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SelectedPresentation.DoesNotExist:
            return Response({"error": "selected presentation not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            selected_presentation = SelectedPresentation.objects.get(pk=pk)
            selected_presentation.delete()
            return Response({"massage": "selected presentation deleted"}, status=status.HTTP_202_ACCEPTED)
        except SelectedPresentation.DoesNotExist:
            return Response({"error": "selected presentation not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": f"{e.args}"}, status=status.HTTP_400_BAD_REQUEST)
