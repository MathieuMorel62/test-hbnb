import sys
import os
import unittest
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from app import create_app
from app.models.amenity import Amenity


class TestAmenitiesEndpoints(unittest.TestCase):
    """Tests pour les endpoints des amenities"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Nettoyer le repository
        from app.api.v1.amenities import facade
        facade.amenity_repo._storage.clear()

    def tearDown(self):
        """Nettoyage après chaque test"""
        self.app_context.pop()

    def test_create_amenity_success(self):
        """Test création d'amenity avec succès"""
        amenity_data = {
            'name': 'Wi-Fi'
        }
        
        response = self.client.post('/api/v1/amenities/', 
                                  data=json.dumps(amenity_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'Wi-Fi')

    def test_create_amenity_invalid_data(self):
        """Test création d'amenity avec données invalides"""
        amenity_data = {
            'name': ''  # Nom vide
        }
        
        response = self.client.post('/api/v1/amenities/', 
                                  data=json.dumps(amenity_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_missing_name(self):
        """Test création d'amenity sans nom"""
        amenity_data = {}
        
        response = self.client.post('/api/v1/amenities/', 
                                  data=json.dumps(amenity_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_long_name(self):
        """Test création d'amenity avec nom trop long"""
        amenity_data = {
            'name': 'A' * 51  # Nom trop long
        }
        
        response = self.client.post('/api/v1/amenities/', 
                                  data=json.dumps(amenity_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_get_amenity_success(self):
        """Test récupération d'amenity par ID"""
        # Créer une amenity d'abord
        amenity_data = {'name': 'Pool'}
        
        create_response = self.client.post('/api/v1/amenities/', 
                                         data=json.dumps(amenity_data),
                                         content_type='application/json')
        
        created_amenity = json.loads(create_response.data)
        amenity_id = created_amenity['id']
        
        # Récupérer l'amenity
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], amenity_id)
        self.assertEqual(data['name'], 'Pool')

    def test_get_amenity_not_found(self):
        """Test récupération d'amenity inexistante"""
        response = self.client.get('/api/v1/amenities/nonexistent-id')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Amenity not found')

    def test_get_all_amenities(self):
        """Test récupération de toutes les amenities"""
        # Créer quelques amenities
        amenities_data = [
            {'name': 'Wi-Fi'},
            {'name': 'Air Conditioning'}
        ]
        
        for amenity_data in amenities_data:
            self.client.post('/api/v1/amenities/', 
                           data=json.dumps(amenity_data),
                           content_type='application/json')
        
        # Récupérer toutes les amenities
        response = self.client.get('/api/v1/amenities/')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    def test_get_all_amenities_empty(self):
        """Test récupération de toutes les amenities avec liste vide"""
        response = self.client.get('/api/v1/amenities/')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

    def test_update_amenity_success(self):
        """Test mise à jour d'amenity avec succès"""
        # Créer une amenity d'abord
        amenity_data = {'name': 'Original Pool'}
        
        create_response = self.client.post('/api/v1/amenities/', 
                                         data=json.dumps(amenity_data),
                                         content_type='application/json')
        
        created_amenity = json.loads(create_response.data)
        amenity_id = created_amenity['id']
        
        # Mettre à jour l'amenity
        update_data = {'name': 'Swimming Pool'}
        
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', 
                                 data=json.dumps(update_data),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Swimming Pool')

    def test_update_amenity_not_found(self):
        """Test mise à jour d'amenity inexistante"""
        update_data = {'name': 'Updated Name'}
        
        response = self.client.put('/api/v1/amenities/nonexistent-id', 
                                 data=json.dumps(update_data),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Amenity not found')

    def test_update_amenity_invalid_data(self):
        """Test mise à jour d'amenity avec données invalides"""
        # Créer une amenity d'abord
        amenity_data = {'name': 'Test Pool'}
        
        create_response = self.client.post('/api/v1/amenities/', 
                                         data=json.dumps(amenity_data),
                                         content_type='application/json')
        
        created_amenity = json.loads(create_response.data)
        amenity_id = created_amenity['id']
        
        # Essayer de mettre à jour avec nom vide
        update_data = {'name': ''}
        
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', 
                                 data=json.dumps(update_data),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_update_amenity_long_name(self):
        """Test mise à jour d'amenity avec nom trop long"""
        # Créer une amenity d'abord
        amenity_data = {'name': 'Test Pool'}
        
        create_response = self.client.post('/api/v1/amenities/', 
                                         data=json.dumps(amenity_data),
                                         content_type='application/json')
        
        created_amenity = json.loads(create_response.data)
        amenity_id = created_amenity['id']
        
        # Essayer de mettre à jour avec nom trop long
        update_data = {'name': 'A' * 51}
        
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', 
                                 data=json.dumps(update_data),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
