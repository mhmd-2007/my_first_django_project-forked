from django.test import TestCase
from app.models import Choice, Survey, Product, Profile
from django.contrib.auth.models import User
from django.db import IntegrityError

class ChoiceModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="هدفون X500",
            description="یک هدفون عالی",
            launch_date="2025-01-15"
        )
        self.survey = Survey.objects.create(
            product=self.product,
            question="کیفیت صدا چطوره؟",
            is_active=True
        )
    
    def test_create_choice(self):
        choice = Choice.objects.create(
            survey=self.survey,
            choice_text="عالی",
            votes=0
        )
        self.assertEqual(choice.choice_text, "عالی")
        self.assertEqual(choice.votes, 0)
        self.assertEqual(str(choice), "عالی")
    
    def test_choice_belongs_to_survey(self):

        choice = Choice.objects.create(
            survey=self.survey,
            choice_text="خوب",
            votes=0
        )
        self.assertEqual(choice.survey.question, "کیفیت صدا چطوره؟")
from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Product, Survey, Choice, Vote, Profile


class ProfileModelTest(TestCase):
    def setUp(self):
    
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
    
    def test_profile_created_automatically_for_new_user(self):   # چک می‌کنیم که کاربر پروفایل دارد
        self.assertTrue(hasattr(self.user, 'profile'))
        
       
        profile_exists = Profile.objects.filter(user=self.user).exists()
        self.assertTrue(profile_exists)

    def test_one_to_one_relation_between_user_and_profile(self):
        with self.assertRaises(IntegrityError):
            Profile.objects.create(user=self.user)

    def test_access_profile_via_related_name(self):
        profile = self.user.profile
        
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user.username, "testuser")
    
    def test_optional_fields_can_be_blank(self):
    
        profile = self.user.profile
        
        self.assertIsNone(profile.bio)
        self.assertIsNone(profile.birth_date)
        self.assertIsNone(profile.phone)
        self.assertIsNone(profile.website)

        self.assertIsNotNone(profile.avatar)
        self.assertEqual(profile.avatar.name, 'avatar/default.jpg')

    def test_update_profile_fields(self):
        profile = self.user.profile
    
        profile.bio = "این یک بیوگرافی تست است"
        profile.phone = "09123456789"
        profile.save()
     
        profile.refresh_from_db()
        
        self.assertEqual(profile.bio, "این یک بیوگرافی تست است")
        self.assertEqual(profile.phone, "09123456789")
    
    def test_profile_str_method(self):
     
        profile = self.user.profile
        expected_str = f"profile user: {self.user.username}"
        self.assertEqual(str(profile), expected_str)

    def test_user_without_profile_raises_error(self):
        from django.db.models.signals import post_save
        from app.signals import create_user_profile

        post_save.disconnect(create_user_profile, sender=User)
        
        new_user = User.objects.create_user(
            username="noprofile",
            password="test123"
        )

        self.assertFalse(hasattr(new_user, 'profile'))
        post_save.connect(create_user_profile, sender=User)