from django.test import TestCase
from django.urls import reverse

class StudentsViewsTest(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/home.html')
        self.assertContains(response, 'Bug Network Private Limited')

    def test_about_page_status_code(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1>About Page</h1>')
        self.assertContains(response, 'Welcome to the About page of our Django application!')

