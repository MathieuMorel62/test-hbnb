import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from app.services.facade import HBnBFacade
from app.models.user import User


class TestHBnBFacade(unittest.TestCase):
    """Tests pour la facade HBnB"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.facade = HBnBFacade()

    def test_create_user(self):
        """Test création d'utilisateur via facade"""
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com'
        }
        
        user = self.facade.create_user(user_data)
        
        self.assertIsInstance(user, User)
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'john.doe@example.com')
        self.assertIsNotNone(user.id)

    def test_get_user(self):
        """Test récupération d'utilisateur par ID"""
        user_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com'
        }
        
        created_user = self.facade.create_user(user_data)
        retrieved_user = self.facade.get_user(created_user.id)
        
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.id, created_user.id)
        self.assertEqual(retrieved_user.first_name, 'Jane')

    def test_get_user_not_found(self):
        """Test récupération d'utilisateur inexistant"""
        user = self.facade.get_user('nonexistent-id')
        self.assertIsNone(user)

    def test_get_all_users(self):
        """Test récupération de tous les utilisateurs"""
        # Créer quelques utilisateurs
        users_data = [
            {'first_name': 'User1', 'last_name': 'Test1', 'email': 'user1@test.com'},
            {'first_name': 'User2', 'last_name': 'Test2', 'email': 'user2@test.com'}
        ]
        
        for user_data in users_data:
            self.facade.create_user(user_data)
        
        all_users = self.facade.get_all_users()
        
        self.assertEqual(len(all_users), 2)
        self.assertIsInstance(all_users[0], User)
        self.assertIsInstance(all_users[1], User)

    def test_get_user_by_email(self):
        """Test récupération d'utilisateur par email"""
        user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test.user@example.com'
        }
        
        created_user = self.facade.create_user(user_data)
        retrieved_user = self.facade.get_user_by_email('test.user@example.com')
        
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.id, created_user.id)
        self.assertEqual(retrieved_user.email, 'test.user@example.com')

    def test_get_user_by_email_not_found(self):
        """Test récupération d'utilisateur par email inexistant"""
        user = self.facade.get_user_by_email('nonexistent@example.com')
        self.assertIsNone(user)

    def test_update_user_success(self):
        """Test mise à jour d'utilisateur avec succès"""
        user_data = {
            'first_name': 'Original',
            'last_name': 'Name',
            'email': 'original@example.com'
        }
        
        created_user = self.facade.create_user(user_data)
        
        update_data = {
            'first_name': 'Updated',
            'last_name': 'NewName'
        }
        
        updated_user = self.facade.update_user(created_user.id, update_data)
        
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.last_name, 'NewName')
        self.assertEqual(updated_user.email, 'original@example.com')  # Email inchangé

    def test_update_user_not_found(self):
        """Test mise à jour d'utilisateur inexistant"""
        update_data = {'first_name': 'Updated'}
        updated_user = self.facade.update_user('nonexistent-id', update_data)
        self.assertIsNone(updated_user)

    def test_update_user_duplicate_email(self):
        """Test mise à jour avec email déjà utilisé"""
        # Créer deux utilisateurs
        user1_data = {'first_name': 'User1', 'last_name': 'Test1', 'email': 'user1@test.com'}
        user2_data = {'first_name': 'User2', 'last_name': 'Test2', 'email': 'user2@test.com'}
        
        user1 = self.facade.create_user(user1_data)
        user2 = self.facade.create_user(user2_data)
        
        # Essayer de mettre à jour user1 avec l'email de user2
        update_data = {'email': 'user2@test.com'}
        
        with self.assertRaises(ValueError) as context:
            self.facade.update_user(user1.id, update_data)
        
        self.assertEqual(str(context.exception), "Email already registered")

    def test_get_place(self):
        """Test récupération d'un lieu par ID"""
        # Test avec un ID inexistant (le repository place est vide)
        place = self.facade.get_place('nonexistent-place-id')
        self.assertIsNone(place)

        # Note: Pas de test de création de place car la méthode create_place 
        # n'est pas encore implémentée (placeholder)

    def test_update_user_with_same_email(self):
        """Test mise à jour d'utilisateur avec le même email (doit fonctionner)"""
        user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com'
        }
        
        created_user = self.facade.create_user(user_data)
        
        # Mettre à jour avec le même email (doit fonctionner car l'email est le même)
        update_data = {
            'first_name': 'Updated',
            'email': 'test@example.com'  # Même email
        }
        
        updated_user = self.facade.update_user(created_user.id, update_data)
        
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.email, 'test@example.com')


if __name__ == '__main__':
    unittest.main()
