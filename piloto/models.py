from uuid import uuid4
from django.db.models import Model
from django.db.models import CharField
from django.db.models import UUIDField
from django.db.models import EmailField
from django.db.models import DateTimeField
from .constants import Event


# TODO: Should this events corresponde to an user/client? or assume its only one user?
class Event(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    action = CharField(
        choices=Event.choices(),
        help_text="Action taken on emails",
        max_length=5
    )
    subject = CharField(
        help_text="Email subject",
        max_length=200
    )
    recipient = EmailField(
        max_length=254,
    )
    timestamp = DateTimeField(auto_now=True)