# profiles/tests/test_urls.py
from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
User = get_user_model()
from profiles.views import ProfileDetailView
from profiles.models import UserProfile

class ProfilesURLTest(TestCase):
    def setUp(self):
        # Crear datos de prueba para la vista de detalle
        self.user = User.objects.create_user(
            username='Test User', 
            email='test@gmail.com', 
            password='password123'
        )
        self.profile = UserProfile.objects.create(user=self.user)

    def test_profile_detail_url_resolves(self):
        """Probar que la URL de detalle resuelve hacia la vista correcta"""
        url = reverse('profiles:detail', kwargs={'user_uuid': str(self.user.uuid)})
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, ProfileDetailView)

    def test_profile_detail_view_404(self):
        """Probar que un perfil inexistente devuelve un 404"""
        self.client.login(username='Test User', password='password123') # Logearse con el profile creado 
        import uuid
        url = reverse('profiles:detail', kwargs={'user_uuid': str(uuid.uuid4())})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
