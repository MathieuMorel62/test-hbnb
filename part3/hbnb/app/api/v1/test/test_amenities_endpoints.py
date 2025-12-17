import sys
import os
import unittest
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from app import create_app
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository


class TestAmenitiesEndpoints(unittest.TestCase):
    """Tests pour les endpoints des amenities"""

    def setUp(self):
        """Configuration avant chaque test"""
        # Créer des repositories en mémoire pour les tests
        user_repo = InMemoryRepository()
        place_repo = InMemoryRepository()
        review_repo = InMemoryRepository()
        amenity_repo = InMemoryRepository()
        
        repositories = {
            'user_repo': user_repo,
            'place_repo': place_repo,
            'review_repo': review_repo,
            'amenity_repo': amenity_repo
        }
        
        self.app = create_app(repositories)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Créer un utilisateur admin pour les tests
        from app.services import facade
        self.admin_user = facade.create_user({
            'first_name': 'Admin',
            'last_name': 'User',
            'email': 'admin@example.com',
            'password': 'admin123',
            'is_admin': True
        })
        self.admin_token = self.get_auth_token('admin@example.com', 'admin123')

    def tearDown(self):
        """Nettoyage après chaque test"""
        self.app_context.pop()
    
    def get_auth_token(self, email='admin@example.com', password='admin123'):
        """Helper pour obtenir un token JWT"""
        login_data = {'email': email, 'password': password}
        response = self.client.post('/api/v1/auth/login',
                                   data=json.dumps(login_data),
                                   content_type='application/json')
        if response.status_code == 200:
            return json.loads(response.data)['access_token']
        return None

    def test_create_amenity_success(self):
        """Test création d'amenity avec succès"""
        amenity_data = {
            'name': 'Wi-Fi'
        }
        
        response = self.client.post('/api/v1/amenities/', 
                                  data=json.dumps(amenity_data),
                                  content_type='application/json',
                                  headers={'Authorization': f'Bearer {self.admin_token}'})
        
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
                                  content_type='application/json',
                                  headers={'Authorization': f'Bearer {self.admin_token}'})
        
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_missing_name(self):
        """Test création d'amenity sans nom"""
        amenity_data = {}
        
        response = self.client.post('/api/v1/amenities/', 
                                  data=json.dumps(amenity_data),
                                  content_type='application/json',
                                  headers={'Authorization': f'Bearer {self.admin_token}'})
        
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_long_name(self):
        """Test création d'amenity avec nom trop long"""
        amenity_data = {
            'name': 'A' * 51  # Nom trop long
        }
        
        response = self.client.post('/api/v1/amenities/', 
                                  data=json.dumps(amenity_data),
                                  content_type='application/json',
                                  headers={'Authorization': f'Bearer {self.admin_token}'})
        
        self.assertEqual(response.status_code, 400)

    def test_get_amenity_success(self):
        """Test récupération d'amenity par ID"""
        # Créer une amenity d'abord
        amenity_data = {'name': 'Pool'}
        
        create_response = self.client.post('/api/v1/amenities/', 
                                         data=json.dumps(amenity_data),
                                         content_type='application/json',
                                         headers={'Authorization': f'Bearer {self.admin_token}'})
        
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
                           content_type='application/json',
                           headers={'Authorization': f'Bearer {self.admin_token}'})
        
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
                                         content_type='application/json',
                                         headers={'Authorization': f'Bearer {self.admin_token}'})
        
        self.assertEqual(create_response.status_code, 201)
        created_amenity = json.loads(create_response.data)
        amenity_id = created_amenity['id']
        
        # Mettre à jour l'amenity
        update_data = {'name': 'Swimming Pool'}
        
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', 
                                 data=json.dumps(update_data),
                                 content_type='application/json',
                                 headers={'Authorization': f'Bearer {self.admin_token}'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Swimming Pool')

    def test_update_amenity_not_found(self):
        """Test mise à jour d'amenity inexistante"""
        update_data = {'name': 'Updated Name'}
        
        response = self.client.put('/api/v1/amenities/nonexistent-id', 
                                 data=json.dumps(update_data),
                                 content_type='application/json',
                                 headers={'Authorization': f'Bearer {self.admin_token}'})
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Amenity not found')

    def test_update_amenity_invalid_data(self):
        """Test mise à jour d'amenity avec données invalides"""
        # Créer une amenity d'abord
        amenity_data = {'name': 'Test Pool'}
        
        create_response = self.client.post('/api/v1/amenities/', 
                                         data=json.dumps(amenity_data),
                                         content_type='application/json',
                                         headers={'Authorization': f'Bearer {self.admin_token}'})
        
        self.assertEqual(create_response.status_code, 201)
        created_amenity = json.loads(create_response.data)
        amenity_id = created_amenity['id']
        
        # Essayer de mettre à jour avec nom vide
        update_data = {'name': ''}
        
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', 
                                 data=json.dumps(update_data),
                                 content_type='application/json',
                                 headers={'Authorization': f'Bearer {self.admin_token}'})
        
        self.assertEqual(response.status_code, 400)

    def test_update_amenity_long_name(self):
        """Test mise à jour d'amenity avec nom trop long"""
        # Créer une amenity d'abord
        amenity_data = {'name': 'Test Pool'}
        
        create_response = self.client.post('/api/v1/amenities/', 
                                         data=json.dumps(amenity_data),
                                         content_type='application/json',
                                         headers={'Authorization': f'Bearer {self.admin_token}'})
        
        self.assertEqual(create_response.status_code, 201)
        created_amenity = json.loads(create_response.data)
        amenity_id = created_amenity['id']
        
        # Essayer de mettre à jour avec nom trop long
        update_data = {'name': 'A' * 51}
        
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', 
                                 data=json.dumps(update_data),
                                 content_type='application/json',
                                 headers={'Authorization': f'Bearer {self.admin_token}'})
        
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_without_admin_token(self):
        """Test qu'un utilisateur non-admin ne peut pas créer une amenity"""
        # Crée un utilisateur normal d'abord
        normal_user_data = {
            'first_name': 'Normal',
            'last_name': 'User',
            'email': 'normal@example.com',
            'password': 'password123'
        }
        from app.services import facade as services_facade
        normal_user = services_facade.create_user(normal_user_data)
        normal_token = self.get_auth_token('normal@example.com', 'password123')
        
        # L'utilisateur normal essaie de créer une amenity
        amenity_data = {'name': 'Wi-Fi'}
        
        response = self.client.post('/api/v1/amenities/', 
                                  data=json.dumps(amenity_data),
                                  content_type='application/json',
                                  headers={'Authorization': f'Bearer {normal_token}'})
        
        # Doit échouer car ce n'est pas un admin
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Admin privileges required')

    def test_create_amenity_without_token(self):
        """Test qu'on ne peut pas créer une amenity sans token JWT"""
        amenity_data = {'name': 'Wi-Fi'}
        
        response = self.client.post('/api/v1/amenities/', 
                                  data=json.dumps(amenity_data),
                                  content_type='application/json')
        
        # Doit échouer car pas de token
        self.assertEqual(response.status_code, 401)

    def test_update_amenity_without_admin_token(self):
        """Test qu'un utilisateur non-admin ne peut pas modifier une amenity"""
        # Crée une amenity d'abord avec l'admin
        amenity_data = {'name': 'Test Pool'}
        create_response = self.client.post('/api/v1/amenities/', 
                                         data=json.dumps(amenity_data),
                                         content_type='application/json',
                                         headers={'Authorization': f'Bearer {self.admin_token}'})
        created_amenity = json.loads(create_response.data)
        amenity_id = created_amenity['id']
        
        # Crée un utilisateur normal
        normal_user_data = {
            'first_name': 'Normal',
            'last_name': 'User',
            'email': 'normal2@example.com',
            'password': 'password123'
        }
        from app.services import facade as services_facade
        normal_user = services_facade.create_user(normal_user_data)
        normal_token = self.get_auth_token('normal2@example.com', 'password123')
        
        # L'utilisateur normal essaie de modifier l'amenity
        update_data = {'name': 'Updated Pool'}
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', 
                                 data=json.dumps(update_data),
                                 content_type='application/json',
                                 headers={'Authorization': f'Bearer {normal_token}'})
        
        # Doit échouer car ce n'est pas un admin
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Admin privileges required')

    def test_update_amenity_without_token(self):
        """Test qu'on ne peut pas modifier une amenity sans token JWT"""
        # Crée une amenity d'abord avec l'admin
        amenity_data = {'name': 'Test Pool'}
        create_response = self.client.post('/api/v1/amenities/', 
                                         data=json.dumps(amenity_data),
                                         content_type='application/json',
                                         headers={'Authorization': f'Bearer {self.admin_token}'})
        created_amenity = json.loads(create_response.data)
        amenity_id = created_amenity['id']
        
        # Essayer de modifier sans token
        update_data = {'name': 'Updated Pool'}
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', 
                                 data=json.dumps(update_data),
                                 content_type='application/json')
        
        # Doit échouer car pas de token
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
