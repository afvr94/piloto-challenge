from datetime import datetime

from django_filters.filters import DateFilter
from django_filters.rest_framework import FilterSet
from django.db.models import QuerySet
from .serializers import StartDateRangeSerializer
from .models import Event


class EventFilter(FilterSet):
    timestamp = DateFilter(method="filter_timestamp")

    def filter_timestamp(
        self, queryset: QuerySet, name: str, value: datetime
    ) -> QuerySet:
        serializer = StartDateRangeSerializer(
            data=self.request.query_params,
        )
        serializer.is_valid(raise_exception=True)
        start_time = serializer.validated_data["start_time"]
        end_time = serializer.validated_data["end_time"]
        return queryset.filter(timestamp__range=(start_time, end_time))

    class Meta:
        model = Event
        fields = ("action", "subject")
