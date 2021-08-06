import pytz
from piloto.constants import EventType
from rest_framework.test import APITestCase
from piloto.models import Event
from datetime import datetime
from unittest import mock


class EventViewSetTest(APITestCase):
    def test_get_events(self):
        Event.objects.create(
            action=EventType.OPEN.value,
            subject="Subscribe now",
            recipient="abdiel017@gmail.com",
        )
        response = self.client.get("/events")

        self.assertEqual(response.data[0].get("action"), "open")
        self.assertEqual(response.data[0].get("subject"), "Subscribe now")
        self.assertEqual(response.data[0].get("recipient"), "abdiel017@gmail.com")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_events_by_action(self):
        Event.objects.create(
            action=EventType.OPEN.value,
            subject="Subscribe now",
            recipient="abdiel017@gmail.com",
        )
        Event.objects.create(
            action=EventType.CLICK.value,
            subject="Read now",
            recipient="abdiel017@gmail.com",
        )
        response = self.client.get("/events?action=open")

        self.assertEqual(response.data[0].get("action"), "open")
        self.assertEqual(response.data[0].get("subject"), "Subscribe now")
        self.assertEqual(response.data[0].get("recipient"), "abdiel017@gmail.com")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_events_failure_invalid_action(self):
        Event.objects.create(
            action=EventType.OPEN.value,
            subject="Subscribe now",
            recipient="abdiel017@gmail.com",
        )
        Event.objects.create(
            action=EventType.CLICK.value,
            subject="Subscribe now",
            recipient="abdiel017@gmail.com",
        )
        response = self.client.get("/events?action=read")

        expected_error = (
            "Select a valid choice. read is not one of the available choices."
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["action"][0], expected_error)

    def test_get_events_by_recipient(self):
        Event.objects.create(
            action=EventType.OPEN.value,
            subject="Subscribe now",
            recipient="abdiel017@gmail.com",
        )
        Event.objects.create(
            action=EventType.CLICK.value,
            subject="Read now",
            recipient="eric.santos@gmail.com",
        )
        response = self.client.get("/events?recipient=eric.santos@gmail.com")

        self.assertEqual(response.data[0].get("action"), "click")
        self.assertEqual(response.data[0].get("subject"), "Read now")
        self.assertEqual(response.data[0].get("recipient"), "eric.santos@gmail.com")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_events_by_timestamp(self):
        mocked = datetime(2021, 8, 20, 12, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            Event.objects.create(
                action=EventType.OPEN.value,
                subject="Subscribe now",
                recipient="abdiel017@gmail.com",
            )
        mocked = datetime(2021, 8, 5, 12, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            Event.objects.create(
                action=EventType.CLICK.value,
                subject="Read now",
                recipient="eric.santos@gmail.com",
            )

        response = self.client.get("/events?timestamp=2021-08-05")

        self.assertEqual(response.data[0].get("action"), "click")
        self.assertEqual(response.data[0].get("subject"), "Read now")
        self.assertEqual(response.data[0].get("recipient"), "eric.santos@gmail.com")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_events_failure_invalid_timestamp(self):
        mocked = datetime(2021, 8, 20, 12, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            Event.objects.create(
                action=EventType.OPEN.value,
                subject="Subscribe now",
                recipient="abdiel017@gmail.com",
            )
        mocked = datetime(2021, 8, 5, 12, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            Event.objects.create(
                action=EventType.CLICK.value,
                subject="Read now",
                recipient="eric.santos@gmail.com",
            )

        response = self.client.get("/events?timestamp=2021-08")

        expected_error = "Enter a valid date."

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["timestamp"][0], expected_error)

    def test_post_event(self):
        pre_count = Event.objects.count()

        data = {
            "action": "click",
            "subject": "Read now",
            "recipient": "eric.santos@gmail.com",
        }

        response = self.client.post("/events", data)

        count = Event.objects.count()

        self.assertEqual(pre_count + 1, count)
        self.assertEqual(response.status_code, 201)


class EventSummaryViewSetTest(APITestCase):
    def setUp(self):
        mocked = datetime(2021, 8, 21, 12, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            Event.objects.create(
                action=EventType.OPEN.value,
                subject="Test 1",
                recipient="abdiel4@gmail.com",
            )
        mocked = datetime(2021, 8, 20, 12, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            Event.objects.create(
                action=EventType.CLICK.value,
                subject="Test 2",
                recipient="abdiel3@gmail.com",
            )
        mocked = datetime(2021, 8, 6, 12, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            Event.objects.create(
                action=EventType.OPEN.value,
                subject="Test 3",
                recipient="abdiel2@gmail.com",
            )
        mocked = datetime(2021, 8, 8, 12, 0, 0, tzinfo=pytz.utc)
        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            Event.objects.create(
                action=EventType.OPEN.value,
                subject="Test 4",
                recipient="abdiel1@gmail.com",
            )

    def test_get_event_summary(self):

        response = self.client.get("/events/summary")

        self.assertEqual(response.data["click"], 1)
        self.assertEqual(response.data["open"], 3)

    def test_get_event_summary_by_recipient(self):

        response = self.client.get("/events/summary?recipient=abdiel1@gmail.com")

        self.assertEqual(response.data["click"], 0)
        self.assertEqual(response.data["open"], 1)

    def test_get_event_summary(self):

        response = self.client.get("/events/summary")

        self.assertEqual(response.data["click"], 1)
        self.assertEqual(response.data["open"], 3)

    def test_get_event_summary_by_date_range(self):

        response = self.client.get(
            "/events/summary?start_date=2021-08-06&end_date=2021-08-08"
        )

        self.assertEqual(response.data["click"], 0)
        self.assertEqual(response.data["open"], 2)

    def test_get_event_summary_failure_invalid_date_range(self):

        # start > end
        response = self.client.get(
            "/events/summary?start_date=2021-08-08&end_date=2021-08-06"
        )

        expected_error = "start date can not be greater than end date"
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["date_range"], expected_error)

    def test_get_event_summary_failure_invalid_date_format(self):

        response = self.client.get(
            "/events/summary?start_date=221-08-0&end_date=2021-08-08"
        )

        expected_error = (
            "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["start_date"][0], expected_error)

    def test_get_event_summary_failure_missing_date(self):

        response = self.client.get("/events/summary?start_date=2021-08-06&end_date=")

        self.assertEqual(response.status_code, 400)
