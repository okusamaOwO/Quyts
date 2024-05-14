from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from .models import Learner

class FlashcardLoginTests(TestCase):
    def setUp(self):
        print("-------------heyHELEOEOLELE")
        self.learner = Learner.objects.create_user(
            username = "test",
            password = "testpass",
            email =  "test@example.com"
        )
    def test_flashcard_addcard_login(self):
        client = Client()

        logged_in = client.login(username="test", password="testpass")
        self.assertTrue(logged_in)

        response = client.get("/")
        self.assertIsNot(response, 200)
# Create your tests here.


