from django.test import TestCase, Client
from django.urls import reverse
from learners.models import Learner
from .models import Quiz, Room, Question

class GameModuleTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.learner = Learner.objects.create_user(
            username="testuser",
            password="testpass",
            email="testuser@example.com"
        )
        self.client.login(username="testuser", password="testpass")
    
    def test_game_page_access(self):
        response = self.client.get(reverse('game:game'))
        self.assertEqual(response.status_code, 200)

    def test_wait_room_access(self):
        response = self.client.get(reverse('game:wait_room'))
        self.assertEqual(response.status_code, 200)

    def test_create_quiz(self):
        quiz_data = {
            "quiz_title": "Test Quiz",
            "quiz_description": "This is a test quiz",
            "questions": [
                {
                    "text": "Question 1?",
                    "answer1": "Answer 1",
                    "answer2": "Answer 2",
                    "answer3": "Answer 3",
                    "answer4": "Answer 4",
                    "correct_answer": 1
                }
            ]
        }
        response = self.client.post(reverse('game:create_quiz'), data=json.dumps(quiz_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Quiz.objects.filter(title="Test Quiz").exists())

    def test_create_room(self):
        quiz = Quiz.objects.create(title="Test Quiz", description="Description", author=self.learner)
        room_data = {
            "room_code": "testroom",
            "room_name": "Test Room",
            "quiz": quiz.id,
            "private": True
        }
        response = self.client.post(reverse('game:create_room'), data=room_data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Room.objects.filter(room_code="testroom").exists())

    def test_room_access(self):
        quiz = Quiz.objects.create(title="Test Quiz", description="Description", author=self.learner)
        room = Room.objects.create(room_code="testroom", room_name="Test Room", host=self.learner, quiz=quiz)
        response = self.client.get(reverse('game:room', args=[room.room_code]))
        self.assertEqual(response.status_code, 200)

from channels.testing import WebsocketCommunicator
from .consumers import RoomConsumer
from django.contrib.auth import get_user_model
import json

class RoomConsumerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')

    async def test_room_consumer(self):
        communicator = WebsocketCommunicator(RoomConsumer.as_asgi(), "/ws/game/testroom/")
        communicator.scope['user'] = self.user
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Test sending a message
        await communicator.send_json_to({"type": "chat", "text": "Hello"})
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], "chat_message")
        self.assertEqual(response['message'], "Hello")

        await communicator.disconnect()