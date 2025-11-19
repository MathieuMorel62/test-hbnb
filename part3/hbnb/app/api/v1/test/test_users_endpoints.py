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
        
        # Crée une nouvelle instance du facade pour chaque test
        from app.api.v1.users import facade
        facade.user_repo._storage.clear()  # Nettoie le repository

    def tearDown(self):
        """Nettoyage après chaque test"""
        self.app_context.pop()
    
    def get_auth_token(self, email='john.doe@example.com', password='password123'):
        """Helper pour obtenir un token JWT"""
        from app.api.v1.users import facade
        # Crée un utilisateur s'il n'existe pas
        user = facade.get_user_by_email(email)
        if not user:
            facade.create_user({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': email,
                'password': password
            })
        
        login_data = {'email': email, 'password': password}
        response = self.client.post('/api/v1/auth/login',
                                   data=json.dumps(login_data),
                                   content_type='application/json')
        if response.status_code == 200:
            return json.loads(response.data)['access_token']
        return None

    def test_create_user_success(self):
        """Test création d'utilisateur avec succès"""
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123'
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
            'email': 'john.doe@example.com',
            'password': 'password123'
        }
        
        # Crée un nouvel utilisateur
        self.client.post('/api/v1/users/', 
                        data=json.dumps(user_data),
                        content_type='application/json')
        
        # Essaye de créer un autre utilisateur avec le même email
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
        # Crée un utilisateur d'abord
        user_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'password': 'password123'
        }
        
        create_response = self.client.post('/api/v1/users/', 
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        
        created_user = json.loads(create_response.data)
        user_id = created_user['id']
        
        # Récupére l'utilisateur
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
        # Crée quelques utilisateurs
        users_data = [
            {'first_name': 'User1', 'last_name': 'Test1', 'email': 'user1@test.com', 'password': 'password123'},
            {'first_name': 'User2', 'last_name': 'Test2', 'email': 'user2@test.com', 'password': 'password123'}
        ]
        
        for user_data in users_data:
            self.client.post('/api/v1/users/', 
                           data=json.dumps(user_data),
                           content_type='application/json')
        
        # Récupère tous les utilisateurs
        response = self.client.get('/api/v1/users/')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    def test_update_user_success(self):
        """Test mise à jour d'utilisateur avec succès"""
        # Crée un nouvel utilisateur d'abord
        user_data = {
            'first_name': 'Original',
            'last_name': 'Name',
            'email': 'original@example.com',
            'password': 'password123'
        }
        
        create_response = self.client.post('/api/v1/users/', 
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        
        created_user = json.loads(create_response.data)
        user_id = created_user['id']
        
        # Obtient un token JWT pour cet utilisateur
        token = self.get_auth_token('original@example.com', 'password123')
        self.assertIsNotNone(token)
        
        # Mise à jour de l'utilisateur (sans email car on ne peut pas le modifier)
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        
        response = self.client.put(f'/api/v1/users/{user_id}', 
                                 data=json.dumps(update_data),
                                 content_type='application/json',
                                 headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'Updated')
        self.assertEqual(data['email'], 'original@example.com')  # Email ne change pas

    def test_update_user_not_found(self):
        """Test mise à jour d'utilisateur inexistant"""
        # Obtient un token JWT
        token = self.get_auth_token()
        self.assertIsNotNone(token)
        
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        
        response = self.client.put('/api/v1/users/nonexistent-id', 
                                 data=json.dumps(update_data),
                                 content_type='application/json',
                                 headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'User not found')

    def test_update_user_duplicate_email(self):
        """Test mise à jour avec email déjà utilisé (ne devrait pas être possible car email ne peut pas être modifié)"""
        # Crée deux utilisateurs
        user1_data = {'first_name': 'User1', 'last_name': 'Test1', 'email': 'user1@test.com', 'password': 'password123'}
        user2_data = {'first_name': 'User2', 'last_name': 'Test2', 'email': 'user2@test.com', 'password': 'password123'}
        
        create_response1 = self.client.post('/api/v1/users/', 
                                          data=json.dumps(user1_data),
                                          content_type='application/json')
        
        create_response2 = self.client.post('/api/v1/users/', 
                                          data=json.dumps(user2_data),
                                          content_type='application/json')
        
        # Vérifie que les créations ont réussies
        self.assertEqual(create_response1.status_code, 201)
        self.assertEqual(create_response2.status_code, 201)
        
        user1_id = json.loads(create_response1.data)['id']
        
        # Obtient un token JWT pour user1
        token = self.get_auth_token('user1@test.com', 'password123')
        self.assertIsNotNone(token)
        
        # Essaye de mettre à jour user1 avec l'email de user2 (ne devrait pas être possible)
        update_data = {
            'first_name': 'User1',
            'last_name': 'Test1',
            'email': 'user2@test.com'  # Email déjà utilisé par user2
        }
        
        response = self.client.put(f'/api/v1/users/{user1_id}', 
                                 data=json.dumps(update_data),
                                 content_type='application/json',
                                 headers={'Authorization': f'Bearer {token}'})
        
        # Doit retourner 400 car on ne peut pas modifier l'email
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'You cannot modify email or password')

    def test_update_user_same_email(self):
        """Test mise à jour avec le même email (ne devrait pas être possible car email ne peut pas être modifié)"""
        # Crée un utilisateur
        user_data = {
            'first_name': 'Original',
            'last_name': 'Name',
            'email': 'original@example.com',
            'password': 'password123'
        }
        
        create_response = self.client.post('/api/v1/users/', 
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        
        created_user = json.loads(create_response.data)
        user_id = created_user['id']
        
        # Obtient un token JWT
        token = self.get_auth_token('original@example.com', 'password123')
        self.assertIsNotNone(token)
        
        # Mise à jour sans email (car on ne peut pas le modifier)
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        
        response = self.client.put(f'/api/v1/users/{user_id}', 
                                 data=json.dumps(update_data),
                                 content_type='application/json',
                                 headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'Updated')
        self.assertEqual(data['email'], 'original@example.com')  # Email reste le même

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

    def test_password_not_returned_in_create_response(self):
        """Test que le mot de passe n'est pas retourné lors de la création"""
        user_data = {
            'first_name': 'Secure',
            'last_name': 'User',
            'email': 'secure@example.com',
            'password': 'super_secret_password'
        }
        
        response = self.client.post('/api/v1/users/', 
                                  data=json.dumps(user_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        
        # Vérifie que le mot de passe n'est pas dans la réponse
        self.assertNotIn('password', data)
        
        # Vérifie que les autres champs sont présents
        self.assertIn('id', data)
        self.assertIn('first_name', data)
        self.assertIn('last_name', data)
        self.assertIn('email', data)

    def test_password_not_returned_in_get_response(self):
        """Test que le mot de passe n'est pas retourné lors de la récupération"""
        # Crée un utilisateur
        user_data = {
            'first_name': 'Test',
            'last_name': 'Password',
            'email': 'testpass@example.com',
            'password': 'my_password_123'
        }
        
        create_response = self.client.post('/api/v1/users/', 
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        
        created_user = json.loads(create_response.data)
        user_id = created_user['id']
        
        # Récupére l'utilisateur
        response = self.client.get(f'/api/v1/users/{user_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Vérifie que le mot de passe n'est pas dans la réponse
        self.assertNotIn('password', data)

    def test_password_not_returned_in_list_response(self):
        """Test que les mots de passe ne sont pas retournés dans la liste"""
        # Crée plusieurs utilisateurs
        users_data = [
            {'first_name': 'User1', 'last_name': 'Pass1', 'email': 'user1pass@test.com', 'password': 'pass1'},
            {'first_name': 'User2', 'last_name': 'Pass2', 'email': 'user2pass@test.com', 'password': 'pass2'}
        ]
        
        for user_data in users_data:
            self.client.post('/api/v1/users/', 
                           data=json.dumps(user_data),
                           content_type='application/json')
        
        # Récupère tous les utilisateurs
        response = self.client.get('/api/v1/users/')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Vérifie qu'aucun utilisateur ne contient de mot de passe
        for user in data:
            self.assertNotIn('password', user)

    def test_create_user_without_password(self):
        """Test création d'utilisateur sans mot de passe"""
        user_data = {
            'first_name': 'No',
            'last_name': 'Password',
            'email': 'nopass@example.com'
        }
        
        response = self.client.post('/api/v1/users/', 
                                  data=json.dumps(user_data),
                                  content_type='application/json')
        
        # Doit échouer car le mot de passe est requis
        self.assertEqual(response.status_code, 400)

    def test_password_not_returned_in_update_response(self):
        """Test que le mot de passe n'est pas retourné lors de la mise à jour"""
        # Crée un nouvel utilisateur
        user_data = {
            'first_name': 'Update',
            'last_name': 'Test',
            'email': 'update@example.com',
            'password': 'initial_password'
        }
        
        create_response = self.client.post('/api/v1/users/', 
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        
        created_user = json.loads(create_response.data)
        user_id = created_user['id']
        
        # Obtient un token JWT
        token = self.get_auth_token('update@example.com', 'initial_password')
        self.assertIsNotNone(token)
        
        # Mise à jour de l'utilisateur (sans email car on ne peut pas le modifier)
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Test'
        }
        
        response = self.client.put(f'/api/v1/users/{user_id}', 
                                 data=json.dumps(update_data),
                                 content_type='application/json',
                                 headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Vérifie que le mot de passe n'est pas dans la réponse
        self.assertNotIn('password', data)
    
    def test_update_user_unauthorized(self):
        """Test qu'un utilisateur ne peut pas modifier un autre utilisateur"""
        # Crée deux utilisateurs
        user1_data = {'first_name': 'User1', 'last_name': 'Test1', 'email': 'user1@test.com', 'password': 'password123'}
        user2_data = {'first_name': 'User2', 'last_name': 'Test2', 'email': 'user2@test.com', 'password': 'password123'}
        
        create_response1 = self.client.post('/api/v1/users/', 
                                          data=json.dumps(user1_data),
                                          content_type='application/json')
        create_response2 = self.client.post('/api/v1/users/', 
                                          data=json.dumps(user2_data),
                                          content_type='application/json')
        
        user1_id = json.loads(create_response1.data)['id']
        user2_id = json.loads(create_response2.data)['id']
        
        # Obtient un token JWT pour user1
        token = self.get_auth_token('user1@test.com', 'password123')
        self.assertIsNotNone(token)
        
        # User1 essaie de modifier user2
        update_data = {
            'first_name': 'Hacked',
            'last_name': 'Name'
        }
        
        response = self.client.put(f'/api/v1/users/{user2_id}', 
                                 data=json.dumps(update_data),
                                 content_type='application/json',
                                 headers={'Authorization': f'Bearer {token}'})
        
        # Doit retourner 403 car user1 ne peut pas modifier user2
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Unauthorized action')
    
    def test_update_user_without_token(self):
        """Test qu'on ne peut pas modifier un utilisateur sans token JWT"""
        # Crée un utilisateur d'abord
        user_data = {
            'first_name': 'Original',
            'last_name': 'Name',
            'email': 'original2@example.com',
            'password': 'password123'
        }
        
        create_response = self.client.post('/api/v1/users/', 
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        
        created_user = json.loads(create_response.data)
        user_id = created_user['id']
        
        # Essayer de modifier sans token
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        
        response = self.client.put(f'/api/v1/users/{user_id}', 
                                 data=json.dumps(update_data),
                                 content_type='application/json')
        
        # Doit échouer car pas de token
        self.assertEqual(response.status_code, 401)
    
    def test_update_user_password(self):
        """Test qu'on ne peut pas modifier le password via PUT"""
        # Crée un utilisateur d'abord
        user_data = {
            'first_name': 'Original',
            'last_name': 'Name',
            'email': 'original3@example.com',
            'password': 'password123'
        }
        
        create_response = self.client.post('/api/v1/users/', 
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        
        created_user = json.loads(create_response.data)
        user_id = created_user['id']
        
        # Obtient un token JWT
        token = self.get_auth_token('original3@example.com', 'password123')
        self.assertIsNotNone(token)
        
        # Essayer de modifier le password
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'password': 'newpassword123'
        }
        
        response = self.client.put(f'/api/v1/users/{user_id}', 
                                 data=json.dumps(update_data),
                                 content_type='application/json',
                                 headers={'Authorization': f'Bearer {token}'})
        
        # Doit échouer car on ne peut pas modifier le password
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'You cannot modify email or password')


if __name__ == '__main__':
    unittest.main()
