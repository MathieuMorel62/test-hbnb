import sys
import os
import unittest
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
from app import create_app
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity

class TestPlacesEndpoints(unittest.TestCase):
    """Tests pour les endpoints des places"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Créer une nouvelle instance du facade pour chaque test
        from app.services import facade
        facade.place_repo._storage.clear()
        facade.user_repo._storage.clear()
        facade.amenity_repo._storage.clear()

        # Créer un utilisateur et des amenities pour les tests
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123'
        }
        response = self.client.post('/api/v1/users/',
                                  data=json.dumps(self.user_data),
                                  content_type='application/json')
        self.user = json.loads(response.data)

        # Créer des amenities
        self.amenities = []
        amenity_names = ['Wi-Fi', 'Air Conditioning', 'Swimming Pool']
        for name in amenity_names:
            response = self.client.post('/api/v1/amenities/',
                                      data=json.dumps({'name': name}),
                                      content_type='application/json')
            self.amenities.append(json.loads(response.data))

    def tearDown(self):
        """Nettoyage après chaque test"""
        self.app_context.pop()

    def test_create_place_success(self):
        """Test création d'une place avec succès"""
        place_data = {
            'title': 'Cozy Apartment',
            'description': 'A nice place to stay',
            'price': 100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': self.user['id'],
            'amenities': [self.amenities[0]['id'], self.amenities[1]['id']]
        }
        
        response = self.client.post('/api/v1/places/',
                                  data=json.dumps(place_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'Cozy Apartment')
        self.assertEqual(data['price'], 100.0)
        self.assertEqual(data['owner_id'], self.user['id'])

    def test_create_place_invalid_owner(self):
        """Test création d'une place avec propriétaire invalide"""
        place_data = {
            'title': 'Invalid Place',
            'description': 'Should fail',
            'price': 100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': 'invalid-id',
            'amenities': [self.amenities[0]['id']]
        }
        
        response = self.client.post('/api/v1/places/',
                                  data=json.dumps(place_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Owner not found')

    def test_create_place_invalid_price(self):
        """Test création d'une place avec prix invalide"""
        place_data = {
            'title': 'Invalid Place',
            'description': 'Should fail',
            'price': -100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': self.user['id'],
            'amenities': [self.amenities[0]['id']]
        }
        
        response = self.client.post('/api/v1/places/',
                                  data=json.dumps(place_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_get_place_success(self):
        """Test récupération d'une place par ID"""
        # Créer une place d'abord
        place_data = {
            'title': 'Test Place',
            'description': 'For testing',
            'price': 100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': self.user['id'],
            'amenities': [self.amenities[0]['id']]
        }
        
        create_response = self.client.post('/api/v1/places/',
                                         data=json.dumps(place_data),
                                         content_type='application/json')
        
        created_place = json.loads(create_response.data)
        
        # Récupérer la place
        response = self.client.get(f'/api/v1/places/{created_place["id"]}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Test Place')
        self.assertEqual(data['owner']['id'], self.user['id'])
        self.assertIsInstance(data['amenities'], list)
        self.assertEqual(len(data['amenities']), 1)

    def test_get_all_places(self):
        """Test récupération de toutes les places"""
        # Créer quelques places
        place_data = {
            'title': 'Test Place',
            'description': 'For testing',
            'price': 100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': self.user['id'],
            'amenities': [self.amenities[0]['id']]
        }
        
        self.client.post('/api/v1/places/',
                        data=json.dumps(place_data),
                        content_type='application/json')
        
        # Récupérer toutes les places
        response = self.client.get('/api/v1/places/')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Test Place')

    def test_update_place_success(self):
        """Test mise à jour d'une place avec succès"""
        # Créer une place d'abord
        place_data = {
            'title': 'Original Place',
            'description': 'Original description',
            'price': 100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': self.user['id'],
            'amenities': [self.amenities[0]['id']]
        }
        
        create_response = self.client.post('/api/v1/places/',
                                         data=json.dumps(place_data),
                                         content_type='application/json')
        
        created_place = json.loads(create_response.data)
        
        # Mettre à jour la place
        update_data = {
            'title': 'Updated Place',
            'price': 150.0,
            'amenities': [amenity['id'] for amenity in self.amenities]
        }
        
        response = self.client.put(f'/api/v1/places/{created_place["id"]}',
                                 data=json.dumps(update_data),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        # Vérifier les modifications
        get_response = self.client.get(f'/api/v1/places/{created_place["id"]}')
        data = json.loads(get_response.data)
        self.assertEqual(data['title'], 'Updated Place')
        self.assertEqual(len(data['amenities']), 3)

    def test_update_place_not_found(self):
        """Test mise à jour d'une place inexistante"""
        update_data = {
            'title': 'Updated Place',
            'price': 150.0
        }
        
        response = self.client.put('/api/v1/places/nonexistent-id',
                                 data=json.dumps(update_data),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 404)

    def test_update_place_invalid_coordinates(self):
        """Test mise à jour d'une place avec coordonnées invalides"""
        # Créer une place d'abord
        place_data = {
            'title': 'Test Place',
            'description': 'For testing',
            'price': 100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': self.user['id'],
            'amenities': [self.amenities[0]['id']]
        }
        
        create_response = self.client.post('/api/v1/places/',
                                         data=json.dumps(place_data),
                                         content_type='application/json')
        
        created_place = json.loads(create_response.data)
        
        # Essayer de mettre à jour avec des coordonnées invalides
        update_data = {
            'latitude': 91.0,  # Invalid latitude
            'longitude': -122.4194
        }
        
        response = self.client.put(f'/api/v1/places/{created_place["id"]}',
                                 data=json.dumps(update_data),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_coordinates(self):
        """Test création d'une place avec coordonnées invalides"""
        place_data = {
            'title': 'Invalid Place',
            'description': 'Should fail',
            'price': 100.0,
            'latitude': 91.0,  # Invalid latitude
            'longitude': -122.4194,
            'owner_id': self.user['id'],
            'amenities': [self.amenities[0]['id']]
        }
        
        response = self.client.post('/api/v1/places/',
                                data=json.dumps(place_data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_amenity(self):
        """Test création d'une place avec amenity invalide"""
        place_data = {
            'title': 'Invalid Place',
            'description': 'Should fail',
            'price': 100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': self.user['id'],
            'amenities': ['invalid-amenity-id']
        }
        
        response = self.client.post('/api/v1/places/',
                                data=json.dumps(place_data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_get_place_not_found(self):
        """Test récupération d'une place inexistante"""
        response = self.client.get('/api/v1/places/nonexistent-id')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Place not found')

    def test_update_place_invalid_price(self):
        """Test mise à jour d'une place avec prix invalide"""
        # Créer une place d'abord
        place_data = {
            'title': 'Test Place',
            'description': 'For testing',
            'price': 100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': self.user['id'],
            'amenities': [self.amenities[0]['id']]
        }
        
        create_response = self.client.post('/api/v1/places/',
                                        data=json.dumps(place_data),
                                        content_type='application/json')
        
        created_place = json.loads(create_response.data)
        
        # Essayer de mettre à jour avec un prix négatif invalide
        update_data = {
            'price': -50.0  # Prix négatif invalide
        }
        
        response = self.client.put(f'/api/v1/places/{created_place["id"]}',
                                data=json.dumps(update_data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_update_place_invalid_amenity(self):
        """Test mise à jour d'une place avec amenity invalide"""
        # Créer une place d'abord
        place_data = {
            'title': 'Test Place',
            'description': 'For testing',
            'price': 100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': self.user['id'],
            'amenities': [self.amenities[0]['id']]
        }
        
        create_response = self.client.post('/api/v1/places/',
                                        data=json.dumps(place_data),
                                        content_type='application/json')
        
        created_place = json.loads(create_response.data)
        
        # Essayer de mettre à jour avec une amenity invalide
        update_data = {
            'amenities': ['invalid-amenity-id']
        }
        
        response = self.client.put(f'/api/v1/places/{created_place["id"]}',
                                data=json.dumps(update_data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_title_with_special_characters(self):
        """Test création d'une place avec caractères spéciaux dans le titre"""
        place_data = {
            'title': "L'appartement #123 & spa",
            'description': "Test with special chars",
            'price': 100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': self.user['id'],
            'amenities': [self.amenities[0]['id']]
        }
        response = self.client.post('/api/v1/places/',
                                data=json.dumps(place_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_description_none(self):
        """Test création d'une place avec description None"""
        place_data = {
            'title': "Valid Place",
            'description': None,
            'price': 100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': self.user['id'],
            'amenities': [self.amenities[0]['id']]
        }
        response = self.client.post('/api/v1/places/',
                                data=json.dumps(place_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    def test_invalid_price_type(self):
        """Test avec un prix qui n'est pas un nombre"""
        place_data = {
            'title': "Invalid Price Type",
            'price': "not a number",
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': self.user['id'],
            'amenities': [self.amenities[0]['id']]
        }
        response = self.client.post('/api/v1/places/',
                                data=json.dumps(place_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_invalid_coordinates_type(self):
        """Test avec des coordonnées qui ne sont pas des nombres"""
        place_data = {
            'title': "Invalid Coordinates",
            'price': 100.0,
            'latitude': "not a number",
            'longitude': -122.4194,
            'owner_id': self.user['id'],
            'amenities': [self.amenities[0]['id']]
        }
        response = self.client.post('/api/v1/places/',
                                data=json.dumps(place_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_malformed_json(self):
        """Test avec un JSON mal formé"""
        response = self.client.post('/api/v1/places/',
                                data="{'bad': json}",
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_empty_json(self):
        """Test avec un JSON vide"""
        response = self.client.post('/api/v1/places/',
                                data="{}",
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
