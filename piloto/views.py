from django.http import HttpResponse

from rest_framework.viewsets import GenericViewSet

from .models import Event
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from .serializers import EventSerializer
from .filters import EventFilter

def index(request):
    return HttpResponse("Server is up")

# TODO: Add summary route (with filter recipient or a startDate/endDate combination.)
# TODO: Add tests
# TODO: Add test-data.json	
class EventViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    serializer_class = EventSerializer
    filterset_class = EventFilter
    queryset = Event.objects.all()