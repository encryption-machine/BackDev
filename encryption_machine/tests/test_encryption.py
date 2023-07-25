from django.urls import reverse
from encryption.models import Encryption
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class EncryptionTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            email="test@test.com",
            password="test_password",
            question='test_question',
            answer='test_answer'
        )
        cls.url = reverse('api:encryption-list')

    def test_encryption_with_valid_data(self):
        """Valid data test no auth user"""
        data = {
            "text": "string",
            "algorithm": "morse",
            "key": "string",
            "is_encryption": True,
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Encryption.objects.count(), 0)

    def test_encryption_with_invalid_algorithms(self):
        """Test not valid algorithm"""
        data = {
            "text": "string",
            "algorithm": "invalid_algorithms",
            "key": "string",
            "is_encryption": True,
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('algorithm', response.data)
        self.assertEqual(
            response.data['algorithm'][0],
            'Шифр содержит неправильное название'
        )

    def test_encryption_with_invalid_key(self):
        """Test not valid key"""
        data = {
            "text": "строка",
            "algorithm": "caesar",
            "key": "2a",
            "is_encryption": True,
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_encryption_with_invalid_user(self):
        """Test  creating a database entry"""
        data = {
            "text": "string",
            "algorithm": "morse",
            "key": "valid_key",
            "is_encryption": True,
        }
        self.client.force_authenticate(EncryptionTest.user)
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Encryption.objects.count(), 1)
