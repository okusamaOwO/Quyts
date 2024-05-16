from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from .models import Post, Comment
from learners.models import Learner

class ForumModuleTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Learner.objects.create_user(
            username="testuser",
            password="testpass",
            email="testuser@example.com"
        )
        self.post = Post.objects.create(
            post_title="Test Post",
            post_content="Test Content",
            pub_date_post=timezone.now()
        )

    def test_forum_homepage_access(self):
        response = self.client.get(reverse("forum:home"))
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        logged_in = self.client.login(username="testuser", password="testpass")
        self.assertTrue(logged_in)
        data = {
            "post_title": "New Test Post",
            "post_content": "New Test Content"
        }
        response = self.client.post(reverse("forum:home"), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful post creation
        self.assertTrue(Post.objects.filter(post_title="New Test Post").exists())

    def test_create_comment(self):
        logged_in = self.client.login(username="testuser", password="testpass")
        self.assertTrue(logged_in)
        data = {
            "comment_context": "Test Comment",
        }
        response = self.client.post(reverse("forum:post_detail", args=[self.post.pk]), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful comment creation
        self.assertTrue(Comment.objects.filter(comment_context="Test Comment", post=self.post).exists())

    def test_like_post(self):
        logged_in = self.client.login(username="testuser", password="testpass")
        self.assertTrue(logged_in)
        response = self.client.post(reverse("forum:like_post", args=[self.post.pk]))
        self.post.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.post_like, 1)

    def test_dislike_post(self):
        logged_in = self.client.login(username="testuser", password="testpass")
        self.assertTrue(logged_in)
        response = self.client.post(reverse("forum:dislike_post", args=[self.post.pk]))
        self.post.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.post_dislike, 1)

