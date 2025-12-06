from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from zoo.models import Habitat, Enclosure
from .models import Feeding


class FeedingAPITestCase(APITestCase):
    def setUp(self):
        """Set up test data before each test"""
        self.habitat = Habitat.objects.create(
            name="African Savanna",
            location="North Wing"
        )
        self.enclosure = Enclosure.objects.create(
            name="Lion Enclosure",
            capacity=6,
            is_active=True,
            habitat=self.habitat
        )
        self.user = User.objects.create_user(
            username='testkeeper',
            password='testpass'
        )
        self.other_user = User.objects.create_user(
            username='otherkeeper',
            password='otherpass'
        )

        # Create a sample feeding
        self.now = timezone.now()
        self.feeding = Feeding.objects.create(
            enclosure=self.enclosure,
            keeper='testkeeper',
            start_time=self.now + timedelta(hours=1),
            end_time=self.now + timedelta(hours=2)
        )

    def test_list_feedings(self):
        """Test retrieving list of feedings"""
        self.client.force_authenticate(user=self.user)
        url = '/api/feedings/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_list_feedings_unauthenticated(self):
        """Test that unauthenticated users cannot list feedings"""
        url = '/api/feedings/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_feeding(self):
        """Test creating a feeding"""
        self.client.force_authenticate(user=self.user)
        url = '/api/feedings/'
        data = {
            'enclosure': self.enclosure.id,
            'keeper': 'testkeeper',
            'start_time': (self.now + timedelta(hours=3)).isoformat(),
            'end_time': (self.now + timedelta(hours=4)).isoformat()
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feeding.objects.count(), 2)

    def test_feeding_validation_end_before_start(self):
        """Test that end time must be after start time"""
        self.client.force_authenticate(user=self.user)
        url = '/api/feedings/'
        data = {
            'enclosure': self.enclosure.id,
            'keeper': 'testkeeper',
            'start_time': self.now.isoformat(),
            'end_time': (self.now - timedelta(hours=1)).isoformat()
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_feeding_overlap_validation(self):
        """Test that overlapping feedings are not allowed"""
        self.client.force_authenticate(user=self.user)
        url = '/api/feedings/'
        # Try to create overlapping feeding
        data = {
            'enclosure': self.enclosure.id,
            'keeper': 'testkeeper',
            'start_time': (
                self.now + timedelta(hours=1, minutes=30)
            ).isoformat(),
            'end_time': (self.now + timedelta(hours=2, minutes=30)).isoformat()
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_by_enclosure(self):
        """Test filtering feedings by enclosure"""
        self.client.force_authenticate(user=self.user)
        url = f'/api/feedings/?enclosure={self.enclosure.id}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_by_date(self):
        """Test filtering feedings by date"""
        self.client.force_authenticate(user=self.user)
        start_date = (self.now + timedelta(hours=1)).date()
        url = f'/api/feedings/?start_date={start_date}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_ordering_by_start_time(self):
        """Test ordering feedings by start time"""
        self.client.force_authenticate(user=self.user)
        # Create another feeding
        Feeding.objects.create(
            enclosure=self.enclosure,
            keeper='testkeeper',
            start_time=self.now + timedelta(hours=5),
            end_time=self.now + timedelta(hours=6)
        )

        url = '/api/feedings/?ordering=start_time'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that results are ordered correctly
        results = response.data['results']
        self.assertLessEqual(
            results[0]['start_time'],
            results[1]['start_time']
        )
