import datetime
from unittest import mock

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from wagtail.core.models import Site

from ..models import ContactFormSubmission, PortfolioSettings

WHITELIST_IP = "18.9.23.9"
BLACKLIST_IP = "3.3.3.3"
LAMBDA_IP = "8.8.8.8"
MIN_DELAY = 60
MAX_ATTEMPT = 2


@override_settings(
    CONTACT_FORM_IP_ADDRESS_BLACKLIST=[BLACKLIST_IP],
    CONTACT_FORM_IP_ADDRESS_WHITELIST=[WHITELIST_IP],
    CONTACT_FORM_MIN_DELAY_SECONDS=MIN_DELAY,
    CONTACT_FORM_MAX_ATTEMPT=MAX_ATTEMPT,
)
class ContactViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        site = Site.objects.get(is_default_site=True)
        PortfolioSettings.objects.get_or_create(
            site=site,
            defaults={
                "email_form": "foo@example.fr",
            },
        )

        cls.url = reverse("contact")

    def tearDown(self):
        ContactFormSubmission.objects.all().delete()

    def test_require_field(self):
        response = self.client.post(self.url, data={}, follow=True)
        self.assertIn("name", response.context_data["form"].errors)
        self.assertIn("email", response.context_data["form"].errors)
        self.assertIn("message", response.context_data["form"].errors)

    @mock.patch("portfolio.core.views.get_client_ip", return_value=(BLACKLIST_IP, False))
    def test_blacklist(self, mock_client_ip):
        with self.assertLogs("portfolio.contact", "INFO"):
            self.client.post(
                self.url,
                follow=True,
                data={
                    "name": "test",
                    "email": "test+1@example.com",
                    "phone": "02 40 40 40 40",
                    "message": "blah blah blah",
                },
            )
        self.assertEqual(ContactFormSubmission.objects.all().count(), 0)

    @mock.patch("portfolio.core.views.get_client_ip", return_value=(WHITELIST_IP, False))
    def test_whitelist(self, mock_client_ip):
        """
        Even if limit is exceed, whitelist can redo it.
        """
        data = {
            "name": "test",
            "email": "test+1@example.com",
            "phone": "02 40 40 40 40",
            "message": "blah blah blah",
        }
        for i in range(0, MAX_ATTEMPT + 1):
            ContactFormSubmission.objects.create(ip_address=WHITELIST_IP, **data)

        self.client.post(self.url, follow=True, data=data)
        self.assertEqual(ContactFormSubmission.objects.all().count(), MAX_ATTEMPT + 2)

    @mock.patch("portfolio.core.views.get_client_ip", return_value=(LAMBDA_IP, False))
    def test_max_attempt_exceed(self, mock_client_ip):
        data = {
            "name": "test",
            "email": "test+1@example.com",
            "phone": "02 40 40 40 40",
            "message": "blah blah blah",
        }
        for i in range(0, MAX_ATTEMPT + 1):
            ContactFormSubmission.objects.create(ip_address=LAMBDA_IP, **data)

        with self.assertLogs("portfolio.contact", "INFO"):
            self.client.post(self.url, follow=True, data=data)

        self.assertEqual(ContactFormSubmission.objects.all().count(), MAX_ATTEMPT + 1)

    @mock.patch("portfolio.core.views.get_client_ip", return_value=(LAMBDA_IP, False))
    def test_timeout_exceed(self, mock_client_ip):
        data = {
            "name": "test",
            "email": "test+1@example.com",
            "phone": "02 40 40 40 40",
            "message": "blah blah blah",
        }

        # Max attemp exceed, but in the past.
        with mock.patch.object(timezone, "now") as mock_tz:
            mock_tz.return_value = timezone.make_aware(
                datetime.datetime(2018, 11, 18, 13, 0, 0), datetime.timezone.utc
            )  # noqa
            for i in range(0, MAX_ATTEMPT + 1):
                ContactFormSubmission.objects.create(ip_address=LAMBDA_IP, **data)

        self.client.post(self.url, follow=True, data=data)
        self.assertEqual(ContactFormSubmission.objects.all().count(), MAX_ATTEMPT + 2)

    def test_send_mail(self):
        data = {
            "name": "test",
            "email": "test+1@example.com",
            "phone": "02 40 40 40 40",
            "message": "blah blah blah",
        }
        self.client.post(self.url, follow=True, data=data)
        self.assertEqual(len(mail.outbox), 1)

    def test_save_submission(self):
        data = {
            "name": "foo bar",
            "email": "foo+1@example.com",
            "phone": "02 40 40 40 40",
            "message": "blah blah blah",
        }
        self.client.post(self.url, follow=True, data=data)
        submission = ContactFormSubmission.objects.first()
        self.assertEqual(data["name"], submission.name)
        self.assertEqual(data["email"], submission.email)
        self.assertEqual(data["phone"], submission.phone)
        self.assertEqual(data["message"], submission.message)
