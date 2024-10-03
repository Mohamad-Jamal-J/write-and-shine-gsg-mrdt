# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from .models import Profile
# from .repository import ProfileRepository
#
# User = get_user_model()
#
#
# class ProfileServiceTest(TestCase):
#
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email='test@example.com', password='password', name='Test User'
#         )
#
#     def test_create_profile(self):
#         """
#         Test profile creation for a new user.
#         """
#         ProfileRepository.create_or_update_profile(
#             user=self.user,
#             bio="This is a test bio",
#             education="Test University",
#             headline="Aspiring Developer"
#         )
#         profile = Profile.objects.get(user=self.user)
#         self.assertEqual(profile.bio, "This is a test bio")
#         self.assertEqual(profile.education, "Test University")
#         self.assertEqual(profile.headline, "Aspiring Developer")
#
#     def test_update_profile(self):
#         """
#         Test updating an existing profile.
#         """
#         profile = Profile.objects.create(user=self.user, bio="Old bio", headline="Old Headline")
#         ProfileRepository.create_or_update_profile(
#             user=self.user,
#             bio="New bio",
#             education="New University",
#             headline="New Headline"  # Updating headline
#         )
#         profile.refresh_from_db()
#         self.assertEqual(profile.bio, "New bio")
#         self.assertEqual(profile.education, "New University")
#         self.assertEqual(profile.headline, "New Headline")
#
#     def test_delete_profile(self):
#         """
#         Test profile deletion.
#         """
#         profile = Profile.objects.create(user=self.user, bio="Test bio", headline="Test Headline")
#         ProfileRepository.delete_profile(self.user)
#         self.assertFalse(Profile.objects.filter(user=self.user).exists())
