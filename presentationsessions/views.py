from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import PresentationSession

from .serializers import PresentationSessionSerializer, PresentationSessionUpdateSerializer

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class PresentationSessionList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        presentation = request.query_params.get('presentation')
        classroom = request.query_params.get('classroom')
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        is_cancelled = request.query_params.get('is_cancelled')
        is_extra = request.query_params.get('is_extra')
        criteria = ((Q(presentation=presentation) if presentation else Q()) &
                    (Q(classroom=classroom) if classroom else Q()) &
                    (Q(start_time__gte=start_time) if start_time else Q()) &
                    (Q(end_time__lte=end_time) if end_time else Q()) &
                    (Q(is_cancelled=is_cancelled) if is_cancelled else Q())&
                    (Q(is_extra=is_extra) if is_extra else Q()))
        paginated_presentation_session = pagination(PresentationSession, size, page, criteria)
        serializer = PresentationSessionSerializer(paginated_presentation_session, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])

    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            serializer = PresentationSessionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)


class PresentationSessionDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            presentation_session = PresentationSession.objects.get(pk=pk)
            serializer = PresentationSessionSerializer(presentation_session)
            return Response(serializer.data)
        except PresentationSession.DoesNotExist:
            return Response({"error": "presentation session not found"} ,status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            presentation_session = PresentationSession.objects.get(pk=pk)
            presentation_session_data = PresentationSessionUpdateSerializer(presentation_session).data
            presentation_session_data.update(request.data)
            serializer = PresentationSessionUpdateSerializer(presentation_session, data=presentation_session_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PresentationSession.DoesNotExist:
            return Response({"error": "presentation session not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            presentation_session = PresentationSession.objects.get(pk=pk)
            presentation_session.delete()
            return Response({"massage": "presentation session deleted"}, status=status.HTTP_204_NO_CONTENT)
        except PresentationSession.DoesNotExist:
            return Response({"error": "presentation session not found"}, status=status.HTTP_404_NOT_FOUND)
