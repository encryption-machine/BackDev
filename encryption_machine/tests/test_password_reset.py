from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User


class PasswordResetTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            email="test@test.com",
            password="test_password",
            question='test_question',
            answer='test_answer'
        )
        cls.url = reverse('api:reset_password-reset-password')

    def test_request_from_unauthorized(self):
        """Availability check for an unauthorized user.

        Post request to endpoint api/v1/users/reset_password available for
        unauthorized user.
        """
        response = self.client.post(
            PasswordResetTest.url,
            data={"email": "test@test.com"},
        )

        self.assertEqual(
            response.status_code,
            200,
            "The endpoint must be available to an unauthorized user",
        )

    def test_correct_respone_fields(self):
        """Endpoint returns correct values."""
        response = self.client.post(
            PasswordResetTest.url,
            data={"email": "test@test.com"}
        )

        self.assertEqual(
            response.data['id'],
            PasswordResetTest.user.id,
            "incorrect id returned",
        )
        self.assertEqual(
            response.data['question'],
            PasswordResetTest.user.question,
            "incorrect question returned",
        )

    def test_incorrect_email(self):
        """Endpoint returns status 400 if email is invalid."""
        response = self.client.post(
            PasswordResetTest.url,
            data={"email": "incorrect@test.com"}
        )

        self.assertEqual(
            response.status_code,
            400,
            "Should return status code 400",
        )


class PasswordResetQuestionTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            email="test@test.com",
            password="test_password",
            question='test_question',
            answer='test_answer'
        )
        cls.url = reverse('api:reset_password-reset-password-question')

    def test_request_from_unauthorized(self):
        """Availability check for an authorized user.

        Post request to endpoint api/v1/users/reset_password_question
        available for unauthorized user.
        """
        response = self.client.post(
            PasswordResetQuestionTest.url,
            data={
                "id": 1,
                "answer": "test_answer"
            },
        )

        self.assertEqual(
            response.status_code,
            200,
            "The endpoint must be available to an unauthorized user",
        )

    def test_correct_respone_fields(self):
        """Endpoint returns correct values."""
        response = self.client.post(
            PasswordResetQuestionTest.url,
            data={
                "id": 1,
                "answer": "test_answer"
            }
        )

        self.assertEqual(
            response.data['id'],
            PasswordResetQuestionTest.user.id,
            "incorrect id returned",
        )
        self.assertIsNotNone(
            response.data.get('token'),
            "incorrect question returned",
        )

    def test_incorrect_answer(self):
        """Endpoint returns status 400 if answer is incorrect."""
        response = self.client.post(
            PasswordResetQuestionTest.url,
            data={
                "id": 1,
                "answer": "incorrect_answer"
            }
        )

        self.assertEqual(
            response.status_code,
            400,
            "Should return status code 400",
        )


class PasswordResetConfirmTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            email="test@test.com",
            password="test_password",
            question='test_question',
            answer='test_answer',
            token='dfdfgfgtyrtyruytiuyhjgjhgfh'
        )
        cls.url = reverse('api:reset_password-reset-password-confirm')

    def test_request_from_unauthorized(self):
        """Availability check for an authorized user.

        Post request to endpoint api/v1/users/reset_password_confirm
        available for unauthorized user.
        """
        response = self.client.post(
            PasswordResetConfirmTest.url,
            data={
                "id": 1,
                "token": "dfdfgfgtyrtyruytiuyhjgjhgfh",
                "new_password": "new_password",
                "re_new_password": "new_password",
            },
        )

        self.assertEqual(
            response.status_code,
            201,
            "The endpoint must be available to an unauthorized user",
        )

    def test_incorrect_fields(self):
        """Endpoint returns status 400 if fields are incorrect."""
        response_incorrect_token = self.client.post(
            PasswordResetConfirmTest.url,
            data={
                "id": 1,
                "token": "incorrect_token",
                "new_password": "new_password",
                "re_new_password": "new_password",
            },
        )

        response_incorrect_id = self.client.post(
            PasswordResetConfirmTest.url,
            data={
                "id": 100,
                "token": "incorrect_token",
                "new_password": "new_password",
                "re_new_password": "new_password",
            },
        )

        response_incorrect_re_password = self.client.post(
            PasswordResetConfirmTest.url,
            data={
                "id": 100,
                "token": "incorrect_token",
                "new_password": "new_password",
                "re_new_password": "incorrect_password",
            },
        )

        self.assertEqual(
            response_incorrect_token.status_code,
            400,
            "Should return status code 400",
        )
        self.assertEqual(
            response_incorrect_id.status_code,
            400,
            "Should return status code 400",
        )
        self.assertEqual(
            response_incorrect_re_password.status_code,
            400,
            "Should return status code 400",
        )
