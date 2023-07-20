from datetime import datetime
from django.urls import reverse
from encryption.utils.morse_code import encode
from encryption.models import Encryption
from rest_framework.test import APITestCase
from users.models import User


class EncryptionHistoryTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            email="test@test.com",
            password="test_password",
            question='test_question',
            answer='test_answer'
        )
        cls.encryption = Encryption.objects.create(
            user=cls.user,
            text='тестовый текст',
            algorithm='morse',
            key=None,
            is_encryption=True
        )
        cls.url = reverse('api:encryption_history-list')

    def test_request_from_authorized(self):
        """Availability check for an authorized user.

        Get request to endpoint api/v1/users/encryptions/me
        available for authorized user.
        """
        self.client.force_authenticate(EncryptionHistoryTest.user)
        response = self.client.get(
            EncryptionHistoryTest.url
        )

        self.assertEqual(
            response.status_code,
            200,
            "The endpoint must be available to an authorized user",
        )

    def test_request_from_unauthorized(self):
        """Availability check for an unauthorized user.

        Get request to endpoint api/v1/users/encryptions/me
        unavailable for unauthorized user.
        """
        response = self.client.get(
            EncryptionHistoryTest.url
        )

        self.assertEqual(
            response.status_code,
            401,
            "The endpoint must be unavailable to an unauthorized user",
        )

    def test_correct_respone_fields(self):
        """Endpoint returns correct values."""
        self.client.force_authenticate(EncryptionHistoryTest.user)
        response = self.client.get(
            EncryptionHistoryTest.url
        )
        correct_data = {
            'text': 'тестовый текст',
            'algorithm': 'morse',
            'key': None,
            'is_encryption': True,
            'encrypted_text': encode('тестовый текст'),
            'date': datetime.strftime(
                EncryptionHistoryTest.encryption.date, '%Y-%m-%dT%H:%M:%S.%fZ'
            )
        }

        for field, value in correct_data.items():
            with self.subTest(field=field):
                self.assertEqual(
                    response.data[0][field],
                    value,
                    f'incorrect data in field "{field}" returned'
                )
