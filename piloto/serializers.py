from datetime import datetime
from datetime import timedelta
from typing import Dict
from typing import Any
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import DateField
from .models import Event
from rest_framework.serializers import Serializer
from dateutil.parser import parse


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
            "id",
            "timestamp",
        )


class StartDateRangeSerializer(Serializer):
    timestamp = DateField()

    def to_internal_value(self, data: Any) -> Dict[str, datetime]:
        """
        Receives a `timestamp` date and generates a dict with
        `start_time` and `end_time`, which are datetimes of
        `start` at 00:00:00 and `end` at 23:59:59, respectively
        (i.e. the range is 1 day from `timestamp`)
        """
        validated_data = super().to_internal_value(data)

        start_string = validated_data["timestamp"].strftime("%Y-%m-%d")

        start_time = parse(start_string)
        end_time = start_time + timedelta(days=1) - timedelta(seconds=1)

        return {"start_time": start_time, "end_time": end_time}


class DateRangeSerializer(Serializer):
    start_date = DateField()
    end_date = DateField()

    def to_internal_value(self, data: Any) -> Dict[str, datetime]:
        """
        Receives `start_date` and `end_date` and validates date
        format is correct.Also, validates that the `start_date`
        is not greater than `end_date`. If valid creates a dict of
        two dates `start_date` at `start_date` 00:00:00 and `end_date`
        at `end_date` 23:59:59.
        """
        validated_data = super().to_internal_value(data)

        start_string = validated_data["start_date"].strftime("%Y-%m-%d")
        end_string = validated_data["end_date"].strftime("%Y-%m-%d")

        if validated_data["start_date"] > validated_data["end_date"]:
            raise ValidationError(
                {"date_range": "start date can not be greater than end date"}
            )

        start_date = parse(start_string)
        end_date = parse(end_string) + timedelta(days=1) - timedelta(seconds=1)

        return {"start_date": start_date, "end_date": end_date}
