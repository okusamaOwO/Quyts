from django.test import TestCase
from django.urls import reverse
from .forms import RegistrationForm
from .models import Learner

class LearnerRegistrationTest(TestCase):

    def test_registration_form_valid(self):
        # Create valid registration data
        valid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'strongpassword',
        }

        # Create a POST request with valid data
        response = self.client.post(reverse('learners:register'), valid_data)
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertRedirects(response, reverse('learners:registration-success'))

        # Check if user is created successfully
        user = Learner.objects.get(username=valid_data['username'])
        self.assertTrue(user.is_active)  # Verify user is active

    def test_registration_duplicate_username(self):
        # Create a user first
        Learner.objects.create_user(username='testuser', email='test@example.com', password='password')

        # Create registration data with duplicate username
        duplicate_data = {
            'username': 'testuser',
            'email': 'another@example.com',
            'password': 'anotherpassword',
        }

        # Create a POST request with duplicate data
        response = self.client.post(reverse('learners:register'), duplicate_data)
        self.assertEqual(response.status_code, 200)  # Check for form rendering
        self.assertContains(response, 'Username already exists!')  # Check for error message


    class LearnerLoginTest(TestCase):

        def setUp(self):
            # Create a user for login testing
            self.user = Learner.objects.create_user(username='testuser', email='test@example.com', password='password')

        def test_login_valid_credentials(self):
            # Login with valid credentials
            login_data = {
                'username': 'testuser',
                'password': 'password',
            }
            response = self.client.post(reverse('learners:login'), login_data)
            self.assertRedirects(response, reverse('flashcards:topic'))
            # Additional checks like session existence can be added here

        def test_login_invalid_credentials(self):
            # Login with invalid password
            invalid_data = {
                'username': 'testuser',
                'password': 'invalidpassword',
            }
            response = self.client.post(reverse('learners:login'), invalid_data)
            self.assertEqual(response.status_code, 200)  # Check for form rendering
            self.assertContains(response, 'Invalid username or password')  # Check for error message