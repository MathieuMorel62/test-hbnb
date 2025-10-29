import sys
import os
import unittest
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
from app import create_app
from app.models.user import User


class TestUsersEndpoints(unittest.TestCase):
    """Tests pour les endpoints des utilisateurs"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Créer une nouvelle instance du facade pour chaque test
        from app.api.v1.users import facade
        facade.user_repo._storage.clear()  # Nettoyer le repository

    def tearDown(self):
        """Nettoyage après chaque test"""
        self.app_context.pop()

    def test_create_user_success(self):
        """Test création d'utilisateur avec succès"""
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com'
        }
        
        response = self.client.post('/api/v1/users/', 
                                  data=json.dumps(user_data),
                                  content_type='application/json')
        
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['last_name'], 'Doe')
        self.assertEqual(data['email'], 'john.doe@example.com')

    def test_create_user_duplicate_email(self):
        """Test création d'utilisateur avec email déjà existant"""
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com'
        }
        
        # Créer le premier utilisateur
        self.client.post('/api/v1/users/', 
                        data=json.dumps(user_data),
                        content_type='application/json')
        
        # Essayer de créer un autre avec le même email
        response = self.client.post('/api/v1/users/', 
                                  data=json.dumps(user_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Email already registered')

    def test_create_user_invalid_data(self):
        """Test création d'utilisateur avec données invalides"""
        user_data = {
            'first_name': '',
            'last_name': 'Doe',
            'email': 'invalid-email'
        }
        
        response = self.client.post('/api/v1/users/', 
                                  data=json.dumps(user_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_get_user_success(self):
        """Test récupération d'utilisateur par ID"""
        # Créer un utilisateur d'abord
        user_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com'
        }
        
        create_response = self.client.post('/api/v1/users/', 
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        
        created_user = json.loads(create_response.data)
        user_id = created_user['id']
        
        # Récupérer l'utilisateur
        response = self.client.get(f'/api/v1/users/{user_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], user_id)
        self.assertEqual(data['first_name'], 'Jane')
        self.assertEqual(data['last_name'], 'Smith')
        self.assertEqual(data['email'], 'jane.smith@example.com')

    def test_get_user_not_found(self):
        """Test récupération d'utilisateur inexistant"""
        response = self.client.get('/api/v1/users/nonexistent-id')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'User not found')

    def test_get_all_users(self):
        """Test récupération de tous les utilisateurs"""
        # Créer quelques utilisateurs
        users_data = [
            {'first_name': 'User1', 'last_name': 'Test1', 'email': 'user1@test.com'},
            {'first_name': 'User2', 'last_name': 'Test2', 'email': 'user2@test.com'}
        ]
        
        for user_data in users_data:
            self.client.post('/api/v1/users/', 
                           data=json.dumps(user_data),
                           content_type='application/json')
        
        # Récupérer tous les utilisateurs
        response = self.client.get('/api/v1/users/')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    def test_update_user_success(self):
        """Test mise à jour d'utilisateur avec succès"""
        # Créer un utilisateur d'abord
        user_data = {
            'first_name': 'Original',
            'last_name': 'Name',
            'email': 'original@example.com'
        }
        
        create_response = self.client.post('/api/v1/users/', 
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        
        created_user = json.loads(create_response.data)
        user_id = created_user['id']
        
        # Mettre à jour l'utilisateur
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com'
        }
        
        response = self.client.put(f'/api/v1/users/{user_id}', 
                                 data=json.dumps(update_data),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'Updated')
        self.assertEqual(data['email'], 'updated@example.com')

    def test_update_user_not_found(self):
        """Test mise à jour d'utilisateur inexistant"""
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com'
        }
        
        response = self.client.put('/api/v1/users/nonexistent-id', 
                                 data=json.dumps(update_data),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'User not found')

    def test_update_user_duplicate_email(self):
        """Test mise à jour avec email déjà utilisé"""
        # Créer deux utilisateurs
        user1_data = {'first_name': 'User1', 'last_name': 'Test1', 'email': 'user1@test.com'}
        user2_data = {'first_name': 'User2', 'last_name': 'Test2', 'email': 'user2@test.com'}
        
        create_response1 = self.client.post('/api/v1/users/', 
                                          data=json.dumps(user1_data),
                                          content_type='application/json')
        
        create_response2 = self.client.post('/api/v1/users/', 
                                          data=json.dumps(user2_data),
                                          content_type='application/json')
        
        # Vérifier que les créations ont réussi
        self.assertEqual(create_response1.status_code, 201)
        self.assertEqual(create_response2.status_code, 201)
        
        user1_id = json.loads(create_response1.data)['id']
        
        # Essayer de mettre à jour user1 avec l'email de user2
        update_data = {
            'first_name': 'User1',
            'last_name': 'Test1',
            'email': 'user2@test.com'  # Email déjà utilisé par user2
        }
        
        response = self.client.put(f'/api/v1/users/{user1_id}', 
                                 data=json.dumps(update_data),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Email already registered')

    def test_update_user_same_email(self):
        """Test mise à jour avec le même email (doit fonctionner)"""
        # Créer un utilisateur
        user_data = {
            'first_name': 'Original',
            'last_name': 'Name',
            'email': 'original@example.com'
        }
        
        create_response = self.client.post('/api/v1/users/', 
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        
        created_user = json.loads(create_response.data)
        user_id = created_user['id']
        
        # Mettre à jour avec le même email
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'original@example.com'  # Même email
        }
        
        response = self.client.put(f'/api/v1/users/{user_id}', 
                                 data=json.dumps(update_data),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'Updated')
        self.assertEqual(data['email'], 'original@example.com')

    def test_get_all_users_empty_list(self):
        """Test récupération de tous les utilisateurs avec liste vide"""
        response = self.client.get('/api/v1/users/')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

    def test_create_user_missing_fields(self):
        """Test création d'utilisateur avec champs manquants"""
        # Test sans first_name
        user_data = {
            'last_name': 'Doe',
            'email': 'test@example.com'
        }
        
        response = self.client.post('/api/v1/users/', 
                                  data=json.dumps(user_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
