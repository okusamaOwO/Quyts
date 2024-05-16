from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from .models import Learner, Subject, Tag, Cards
from django.urls import reverse

class FlashcardModuleTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.learner = Learner.objects.create_user(
            username = "test",
            password = "testpass",
            email =  "test@example.com"
        )
    def test_flashcard_homepage_access(self):
        response = self.client.get("/")
        self.assertIs(response.status_code, 200)
    def test_flashcard_addcard_access(self):
        logged_in = self.client.login(username="test", password="testpass")
        self.assertTrue(logged_in)

        response = self.client.get("/flashcards/addCard/")
        self.assertIs(response.status_code, 200)
    def test_flashcard_addtag_access(self):
        logged_in = self.client.login(username="test", password="testpass")
        self.assertTrue(logged_in)

        response = self.client.get("/flashcards/addTag/")
        self.assertIs(response.status_code, 200)
    def test_flashcard_delcard_access(self):
        logged_in = self.client.login(username="test", password="testpass")
        self.assertTrue(logged_in)

        response = self.client.get("/flashcards/delCard/")
        self.assertIs(response.status_code, 200)
    def test_flashcard_deltag_access(self):
        logged_in = self.client.login(username="test", password="testpass")
        self.assertTrue(logged_in)

        response = self.client.get("/flashcards/delTag/")
        self.assertIs(response.status_code, 200)
    def test_add_tag_view(self):
        subject = Subject.objects.create(name='Test Subject')
        logged_in = self.client.login(username="test", password="testpass")
        data = {
            'subject': subject,
            'tagName': 'Test Tag'
        }
        response = self.client.post(reverse('flashcards:addTag'), data)
        self.assertRedirects(response, reverse('flashcards:addCard') + '?inform_message=Create a new set successfully. Add some cards to your set.')
        tag = Tag.objects.get(name='Test Tag', subject=subject, owner=self.learner)
        self.assertIsNotNone(tag)
    def test_add_tag_view_invalid_data(self):
        logged_in = self.client.login(username="test", password="testpass")
        data = {
            'subject': '',
            'tagName': ''
        }
        response = self.client.post(reverse('flashcards:addTag'), data)
        self.assertEqual(response.status_code, 200)
    def test_delete_tag_view(self):
        subject = Subject.objects.create(name='Test Subject')
        self.client.login(username='test', password='testpass')
        tag = Tag.objects.create(
            name='Test Tag',
            subject=subject,
            owner=self.learner
        )
        response = self.client.post(reverse('flashcards:delTag'), data={'tagName': tag.name})
        self.assertRedirects(response, reverse('flashcards:delTag') + "?inform_message=Done")
        self.assertFalse(Tag.objects.filter(name=tag.name).exists())

        learner2 = Learner.objects.create_user(
            username = "test2",
            password = "testpass",
            email =  "test2@example.com"
        )
        client2 = Client()
        client2.login(username='test2', password='testpass')

    def test_add_card_view(self):
        subject = Subject.objects.create(name='Test Subject')
        tag = Tag.objects.create(name='Test Tag', subject=subject, owner=self.learner)
        self.client.login(username='test', password='testpass')
        data = {
            'subject': subject,
            'tagName': 'Test Tag',
            'question': 'meomeo',
            'answer': 'gau',
        }
        response = self.client.post(reverse('flashcards:addCard'), data)
        self.assertRedirects(response, reverse('flashcards:addCard') + '?inform_message=Submitted successfully')
        card = Cards.objects.get(question='meomeo', answer='gau')
        self.assertIsNotNone(card)
        self.assertEqual(card.tag.name, 'Test Tag')
        self.assertEqual(card.tag.subject.name, 'Test Subject')

    def test_delete_card_view(self):
        subject = Subject.objects.create(name='Test Subject')
        tag = Tag.objects.create(name='Test Tag', subject=subject, owner=self.learner)
        card = Cards.objects.create(question='What is the capital of France?', answer='Paris', tag=tag)
        self.client.login(username='test', password='testpass')
        data = {'question': card.question, 'answer': card.answer, 'tagName': tag.name}
        response = self.client.post(reverse('flashcards:delCard'), data)
        self.assertRedirects(response, reverse('flashcards:delCard') + "?inform_message=Done")
        self.assertFalse(Cards.objects.filter(question=card.question, answer=card.answer).exists())


