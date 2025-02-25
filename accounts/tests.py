from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


# 1 - Unit Tests
class UserModelTest(TestCase):
    def test_create_user(self):
        """Foydalanuvchini yaratish test qilinadi"""
        user = User.objects.create(email="test@example.com")
        user.set_password("testpass")
        user.save()
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass"))


class UserRegisterSerializerTest(TestCase):
    def test_validate_email(self):
        """Email unique bo'lishini tekshirish"""
        user = User.objects.create(email="existing@example.com")
        user.set_password("testpass")
        user.save()
        data = {"email": "existing@example.com", "password": "testpass"}

        from accounts.serializers import UserRegisterSerializer
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("user with this email already exists.", serializer.errors["email"])


# 2 - API Tests
class UserAPITest(APITestCase):
    """User rp'yxatdan o'tishi API orqali test qilinadi"""
    def test_register_user(self):
        data = {
            "email": "ogabek@mail.ru",
            "first_name": "Og'abek",
            "last_name": "Murodullayev",
            "password": "testpass"
        }

        response = self.client.post("/auth/register/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_login_user(self):
        """User login qilishi test orqali tekshiriladi"""
        user  = User.objects.create(email="ogabek@mail.ru")
        user.set_password("testpass")
        user.save()

        data = {"email": "ogabek@mail.ru", "password": "testpass"}
        response = self.client.post("/auth/login/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)


# 3 - Integration Tests
class UserFlowTest(APITestCase):
    """User avval ro'yxatdan o'tkaziladi va keyin login qilishi test qilinadi"""
    def test_register_and_login(self):
        data = {
            "email": "ogabek@mail.ru",
            "first_name": "Og'abek",
            "last_name": "Murodullayev",
            "password": "testpass"
        }

        reg_response = self.client.post("/auth/register/", data=data)
        self.assertEqual(reg_response.status_code, status.HTTP_201_CREATED)

        login_data = {"email": "ogabek@mail.ru", "password": "testpass"}
        login_response = self.client.post("/auth/login/", data=login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)