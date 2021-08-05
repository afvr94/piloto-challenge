from rest_framework.serializers import ModelSerializer
from .models import Event

class EventSerializer(ModelSerializer):

    class Meta:
        model = Event
        fields = (
            "id",
            "action",
            "subject",
            "recipient",
            "timestamp",
        )
        read_only_fields = (
            "id", "timestamp",
        )
