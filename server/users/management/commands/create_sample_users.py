from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create sample users for JWT authentication'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample users...')

        # Clear existing users (except superusers)
        User.objects.filter(is_superuser=False).delete()

        # Create sample users
        users_data = [
            {
                'username': 'keeper1',
                'email': 'keeper1@zoo.com',
                'password': 'password123',
                'first_name': 'Sarah',
                'last_name': 'Johnson'
            },
            {
                'username': 'keeper2',
                'email': 'keeper2@zoo.com',
                'password': 'password123',
                'first_name': 'Michael',
                'last_name': 'Chen'
            },
            {
                'username': 'keeper3',
                'email': 'keeper3@zoo.com',
                'password': 'password123',
                'first_name': 'Emma',
                'last_name': 'Wilson'
            },
        ]

        created_users = []
        for user_data in users_data:
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            created_users.append(user)
            self.stdout.write(
                f'  Created user: {user.username}'
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {len(created_users)} users\n'
            )
        )

        self.stdout.write('\nYou can now use these credentials:\n')
        for user in created_users:
            self.stdout.write(
                f'  Username: {user.username}\n'
                f'  Password: password123\n'
            )
