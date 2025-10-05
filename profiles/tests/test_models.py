from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()
from profiles.models import UserProfile 

class UserProfileTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='john', 
            email='john-test@gmail.com', 
            password='password123'
        )

        self.user2 = User.objects.create_user(
            username='mike', 
            email='mike-test@gmail.com', 
            password='password456'
        )

        self.assert_profile1 = UserProfile.objects.create(
            user=self.user1,
            bio="I'm a guitar player",
        )

        self.profile2 = UserProfile.objects.create(
            user=self.user2,
            bio="I'm a football player"
        )

    def test_create_user_profile(self):
        john = UserProfile.objects.get(user=self.user1)
        mike = UserProfile.objects.get(user=self.user2)
        self.assertEqual(john.bio, "I'm a guitar player")
        self.assertEqual(mike.bio, "I'm a football player")
        
        