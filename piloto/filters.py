from django_filters.rest_framework import FilterSet
from .models import Event

# TODO: Add filter by timestamp (with validations)
class EventFilter(FilterSet):
    class Meta:
        model = Event
        fields = ('action', 'subject')