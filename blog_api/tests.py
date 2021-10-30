from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from blog.models import Post, Category
from django.contrib.auth.models import User


class PostTests(APITestCase):
    def test_view_posts(self):
        """
        Ensure we can view all objects.
        """
        url = reverse("blog_api:listcreate")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        """
        Ensure we can create a new Post object
        """
        self.test_category = Category.objects.create(name="django")
        self.testuser1 = User.objects.create_superuser(
            username="test_user1", password="123456789")

        self.client.login(username=self.testuser1.username,
                          password="123456789")

        data = {"title": "new", "author": 1,
                "excerpt": "new", "content": "new"}
        url = reverse("blog_api:listcreate")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_detail(self):
        """
        Ensure we can view a Post object
        """
        self.test_category = Category.objects.create(name="django")
        self.testuser1 = User.objects.create_user(
            username="test_user1", password="123456789")
        test_post = Post.objects.create(category_id=1, title="Post title", excerpt="Post excerpt",
                                        content="Post content", slug="post-title", author_id=1, status="published")
        url = reverse(('blog_api:detailcreate'), kwargs={'pk': 1})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post(self):
        """
        Ensure that only the author of the post 
        can update the Post object
        """

        self.test_category = Category.objects.create(name="django")
        self.testuser1 = User.objects.create_user(
            username="test_user1", password="123456789")
        self.testuser2 = User.objects.create_user(
            username="test_user2", password="123456789")

        test_post = Post.objects.create(category_id=1, title="Post title", excerpt="Post excerpt",
                                        content="Post content", slug="post-title", author_id=1, status="published")

        self.client.login(username=self.testuser2.username,
                     password="123456789")

        url = reverse(('blog_api:detailcreate'), kwargs={'pk': 1})
        data = {"id": 1, "author": 1, "title": "new",
                "excerpt": "new", "content": "new", "status": "published"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()

        self.client.login(username=self.testuser1.username,
                     password="123456789")
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
