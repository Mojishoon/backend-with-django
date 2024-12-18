from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Presentation

from .serializers import PresentationSerializer, PresentationUpdateSerializer

from institutemanager.dependencies import pagination

from django.db.models import Q

from django.db import IntegrityError

class PresentationList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        size = request.query_params.get('size', 20)
        page = request.query_params.get('page', 1)
        course = request.query_params.get('course')
        teacher = request.query_params.get('teacher')
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')
        is_private = request.query_params.get('is_private')
        if teacher or course or from_date or to_date or is_private:
            criteria = ((Q(course=course) if course else Q()) &
                        (Q(teacher=teacher) if teacher else Q()) &
                        (Q(start_date__gte=from_date) if from_date else Q()) &
                        (Q(end_date__lte=to_date) if to_date else Q()) &
                        (Q(is_private=is_private) if is_private else Q()))
        else:
            criteria = Q()
        paginated_presentation = pagination(Presentation, size, page, criteria)
        serializer = PresentationSerializer(paginated_presentation, many=True)
        return Response(serializer.data + [{"size": size, "page": page}])

    def post(self, request):
        try:
            request.data["record_date"] = datetime.today().strftime('%Y-%m-%d')
            request.data["recorder_id"] = request.user.id
            serializer = PresentationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)


class PresentationDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            presentation = Presentation.objects.get(pk=pk)
            serializer = PresentationSerializer(presentation)
            return Response(serializer.data)
        except Presentation.DoesNotExist:
            return Response({"error": "presentation not found"} ,status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
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
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            presentation = Presentation.objects.get(pk=pk)
            presentation.delete()
            return Response({"massage": "presentation deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Presentation.DoesNotExist:
            return Response({"error": "presentation not found"}, status=status.HTTP_404_NOT_FOUND)
