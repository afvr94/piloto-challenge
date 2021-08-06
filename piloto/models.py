from uuid import uuid4
from django.db.models import Model
from django.db.models import CharField
from django.db.models import UUIDField
from django.db.models import EmailField
from django.db.models import DateTimeField
from .constants import EventType


class Event(Model):
    """
    Represents event that can be made to an email
    """

    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    action = CharField(
        choices=EventType.choices(), help_text="Action taken on email", max_length=5
    )
    subject = CharField(help_text="Email subject", max_length=200)
    recipient = EmailField(
        help_text="Email address",
        max_length=254,
    )
    timestamp = DateTimeField(auto_now=True, help_text="Timestamp of the event")
