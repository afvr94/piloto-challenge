from piloto.constants import EventType
from django.http import HttpResponse

from rest_framework.viewsets import GenericViewSet
from typing import Dict
from rest_framework import status

from .models import Event
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from .serializers import EventSerializer
from .filters import EventFilter
from .serializers import DateRangeSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import action


def index(request):
    return HttpResponse("Server is up")


# TODO: Add tests
# TODO: Add test-data.json
class EventViewSet(
    GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin
):
    serializer_class = EventSerializer
    filterset_class = EventFilter
    queryset = Event.objects.all()

    @action(detail=False, methods=["GET"])
    def summary(self, request: Request) -> Response:
        """
        Event summary route to get count of actions (open, click).
        Can use the "recipient" query param to by email recipient,
        and/or a combination of start_date/end_date.
        """
        # Fetch start/end from query params
        start_date = self.request.query_params.get("start_date", None)
        end_date = self.request.query_params.get("end_date", None)
        # Fetch recipient from query params
        recipient = self.request.query_params.get("recipient", None)

        if start_date is None and end_date is not None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if end_date is None and start_date is not None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        summary_data: Dict[str, int] = {}

        queryset = Event.objects.all()
        queryset = self.filter_queryset(queryset)

        if start_date and end_date:
            serializer = DateRangeSerializer(
                data=self.request.query_params,
            )
            serializer.is_valid(raise_exception=True)
            start_date = serializer.validated_data["start_date"]
            end_date = serializer.validated_data["end_date"]
            queryset = queryset.filter(timestamp__range=[start_date, end_date])

        if recipient:
            queryset = queryset.filter(recipient=recipient)

        click_count = queryset.filter(action=EventType.CLICK.value).count()
        open_count = queryset.filter(action=EventType.OPEN.value).count()

        summary_data["click"] = click_count
        summary_data["open"] = open_count

        return Response(summary_data)
