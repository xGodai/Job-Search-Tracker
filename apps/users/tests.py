from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_job_seeker)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


class AuthViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_register_view(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_view(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
    
    def test_user_login(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertRedirects(response, reverse('home'))

    def test_profile_view_renders_when_logged_in(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:profile'))
        # Profile now redirects to home (dashboard)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_profile_requires_login_then_renders(self):
        profile_url = reverse('users:profile')
        login_url = reverse('users:login')
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(login_url, response.url)
        # Login with next pointing to profile should redirect there
        response = self.client.post(f"{login_url}?next={profile_url}", {
            'username': 'testuser',
            'password': 'testpass123'
        }, follow=False)
        # Should redirect to profile_url
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, profile_url)

    def test_dashboard_requires_login(self):
        dashboard_url = reverse('users:dashboard')
        response = self.client.get(dashboard_url)
        self.assertEqual(response.status_code, 302)
        # Dashboard now redirects to home
        # But if not logged in, the @login_required decorator redirects to login first
        self.assertIn(reverse('users:login'), response.url)

    def test_external_next_ignored(self):
        login_url = reverse('users:login')
        malicious_next = 'https://evil.com/phish'
        response = self.client.post(f"{login_url}?next={malicious_next}", {
            'username': 'testuser',
            'password': 'testpass123'
        })
        # Should ignore external next and go to home
        self.assertRedirects(response, reverse('home'))