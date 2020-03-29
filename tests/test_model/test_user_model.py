from django.test import TestCase
from app.models import User
from model_mommy import mommy


class TestUserModel(TestCase):

    def test_can_create_user(self):
        user = mommy.prepare('app.User')
        User.objects.create(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password,
            image=user.image,
            updated_at=user.updated_at,
            phone_number=user.phone_number
        )

        self.assertEqual(User.objects.all().count(), 1)
        self.assertIsInstance(User.objects.get(pk=1), User)
        self.assertEqual(User.objects.get(pk=1).email, user.email)

    def test_can_retrieve_users(self):
        mommy.make('app.User', _quantity=10)

        users = User.objects.all()

        self.assertEqual(users.count(), 10)

    def test_can_update_user(self):
        mommy.make('app.User')

        user = User.objects.first()
        user.image = 'hjwehhjevdvedhnvedhmn'
        user.save()

        self.assertEqual(User.objects.get(pk=13).image, 'hjwehhjevdvedhnvedhmn')

    def test_can_delete_users(self):
        mommy.make('app.User')

        user = User.objects.first()
        user.delete()

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=user.id)