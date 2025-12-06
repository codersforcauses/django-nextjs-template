from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Habitat, Enclosure


class EnclosureAPITestCase(APITestCase):
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
            username='testuser',
            password='testpass123'
        )
        self.admin = User.objects.create_user(
            username='admin',
            password='adminpass123',
            is_staff=True
        )
    
    def test_list_enclosures(self):
        """Test retrieving list of enclosures"""
        url = '/api/enclosures/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            response.data['results'][0]['name'],
            'Lion Enclosure'
        )
    
    def test_retrieve_enclosure(self):
        """Test retrieving a single enclosure"""
        url = f'/api/enclosures/{self.enclosure.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Lion Enclosure')
        self.assertEqual(response.data['capacity'], 6)
    
    def test_create_enclosure_unauthenticated(self):
        """Test that unauthenticated users cannot create enclosures"""
        url = '/api/enclosures/'
        data = {
            'name': 'New Enclosure',
            'capacity': 4,
            'is_active': True,
            'habitat_id': self.habitat.id
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_enclosure_non_admin(self):
        """Test that non-admin users cannot create enclosures"""
        self.client.force_authenticate(user=self.user)
        url = '/api/enclosures/'
        data = {
            'name': 'New Enclosure',
            'capacity': 4,
            'is_active': True,
            'habitat_id': self.habitat.id
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_enclosure_admin(self):
        """Test creating an enclosure as an admin"""
        self.client.force_authenticate(user=self.admin)
        url = '/api/enclosures/'
        data = {
            'name': 'New Enclosure',
            'capacity': 4,
            'is_active': True,
            'habitat_id': self.habitat.id
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enclosure.objects.count(), 2)
        self.assertEqual(response.data['name'], 'New Enclosure')
    
    def test_update_enclosure(self):
        """Test updating an enclosure"""
        self.client.force_authenticate(user=self.admin)
        url = f'/api/enclosures/{self.enclosure.id}/'
        data = {
            'name': 'Updated Enclosure Name',
            'capacity': 8,
            'is_active': True,
            'habitat_id': self.habitat.id
        }
        response = self.client.put(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.enclosure.refresh_from_db()
        self.assertEqual(self.enclosure.name, 'Updated Enclosure Name')
        self.assertEqual(self.enclosure.capacity, 8)
    
    def test_delete_enclosure(self):
        """Test deleting an enclosure"""
        self.client.force_authenticate(user=self.admin)
        url = f'/api/enclosures/{self.enclosure.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Enclosure.objects.count(), 0)
    
    def test_filter_by_capacity(self):
        """Test filtering enclosures by capacity"""
        Enclosure.objects.create(
            name="Elephant Enclosure",
            capacity=10,
            is_active=True,
            habitat=self.habitat
        )
        url = '/api/enclosures/?min_capacity=8'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            response.data['results'][0]['name'],
            'Elephant Enclosure'
        )
    
    def test_search_enclosures(self):
        """Test searching enclosures by name"""
        url = '/api/enclosures/?search=Lion'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_order_enclosures(self):
        """Test ordering enclosures"""
        Enclosure.objects.create(
            name="Ape Enclosure",
            capacity=4,
            is_active=True,
            habitat=self.habitat
        )
        url = '/api/enclosures/?ordering=name'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], 'Ape Enclosure')
    
    def test_inactive_enclosures_not_in_list(self):
        """Test that inactive enclosures are not shown in list"""
        inactive_enclosure = Enclosure.objects.create(
            name="Inactive Enclosure",
            capacity=2,
            is_active=False,
            habitat=self.habitat
        )
        url = '/api/enclosures/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        # Should not include inactive enclosure
        self.assertNotIn(
            inactive_enclosure.name,
            [r['name'] for r in response.data['results']]
        )
    
    def test_nested_habitat_serializer(self):
        """Test that habitat details are nested in response"""
        url = f'/api/enclosures/{self.enclosure.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('habitat', response.data)
        self.assertEqual(
            response.data['habitat']['name'],
            'African Savanna'
        )


class HabitatAPITestCase(APITestCase):
    def setUp(self):
        """Set up test data before each test"""
        self.habitat = Habitat.objects.create(
            name="Reptile House",
            location="South Wing"
        )
    
    def test_list_habitats(self):
        """Test retrieving list of habitats"""
        url = '/api/habitats/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_retrieve_habitat(self):
        """Test retrieving a single habitat"""
        url = f'/api/habitats/{self.habitat.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Reptile House')
