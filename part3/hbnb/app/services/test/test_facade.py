import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from app.services.facade import HBnBFacade
from app.models.user import User
from app.models.place import Place
from app.models.review import Review


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
            'email': 'john.doe@example.com',
            'password': 'password123'
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
            'email': 'jane.smith@example.com',
            'password': 'password123'
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
            {'first_name': 'User1', 'last_name': 'Test1', 'email': 'user1@test.com', 'password': 'password123'},
            {'first_name': 'User2', 'last_name': 'Test2', 'email': 'user2@test.com', 'password': 'password123'}
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
            'email': 'test.user@example.com',
            'password': 'password123'
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
            'email': 'original@example.com',
            'password': 'password123'
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
        user1_data = {'first_name': 'User1', 'last_name': 'Test1', 'email': 'user1@test.com', 'password': 'password123'}
        user2_data = {'first_name': 'User2', 'last_name': 'Test2', 'email': 'user2@test.com', 'password': 'password123'}
        
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
            'email': 'test@example.com',
            'password': 'password123'
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


    def test_create_review(self):
        """Test création d'une review via facade"""
        # Créer un utilisateur et un lieu pour la review
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123'
        }
        user = self.facade.create_user(user_data)

        place_data = {
            'title': 'Test Place',
            'description': 'Test Description',
            'price': 100.0,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'owner_id': user.id
        }
        place = self.facade.create_place(place_data)

        # Créer la review
        review_data = {
            'text': 'Great place!',
            'rating': 5,
            'user_id': user.id,
            'place_id': place.id
        }
        
        review = self.facade.create_review(review_data)
        
        self.assertIsInstance(review, Review)
        self.assertEqual(review.text, 'Great place!')
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.user.id, user.id)
        self.assertEqual(review.place.id, place.id)

    def test_get_review(self):
        """Test récupération d'une review par ID"""
        # Créer les données nécessaires
        user = self.facade.create_user({
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'password123'
        })
        place = self.facade.create_place({
            'title': 'Test Place',
            'description': 'Description',
            'price': 100.0,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'owner_id': user.id
        })
        review_data = {
            'text': 'Test review',
            'rating': 4,
            'user_id': user.id,
            'place_id': place.id
        }
        created_review = self.facade.create_review(review_data)
        
        # Tester la récupération
        retrieved_review = self.facade.get_review(created_review.id)
        
        self.assertIsNotNone(retrieved_review)
        self.assertEqual(retrieved_review.id, created_review.id)
        self.assertEqual(retrieved_review.text, 'Test review')
        self.assertEqual(retrieved_review.rating, 4)

    def test_get_all_reviews(self):
        """Test récupération de toutes les reviews"""
        # Créer les données nécessaires
        user = self.facade.create_user({
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'password123'
        })
        place = self.facade.create_place({
            'title': 'Test Place',
            'description': 'Description',
            'price': 100.0,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'owner_id': user.id
        })

        # Créer plusieurs reviews
        reviews_data = [
            {'text': 'Review 1', 'rating': 4, 'user_id': user.id, 'place_id': place.id},
            {'text': 'Review 2', 'rating': 5, 'user_id': user.id, 'place_id': place.id}
        ]
        
        for review_data in reviews_data:
            self.facade.create_review(review_data)
        
        all_reviews = self.facade.get_all_reviews()
        
        self.assertEqual(len(all_reviews), 2)
        self.assertIsInstance(all_reviews[0], Review)
        self.assertIsInstance(all_reviews[1], Review)

    def test_get_reviews_by_place(self):
        """Test récupération des reviews d'un lieu"""
        # Créer les données nécessaires
        user = self.facade.create_user({
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'password123'
        })
        place = self.facade.create_place({
            'title': 'Test Place',
            'description': 'Description',
            'price': 100.0,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'owner_id': user.id
        })

        # Créer des reviews pour le lieu
        reviews_data = [
            {'text': 'Review 1', 'rating': 4, 'user_id': user.id, 'place_id': place.id},
            {'text': 'Review 2', 'rating': 5, 'user_id': user.id, 'place_id': place.id}
        ]
        
        for review_data in reviews_data:
            self.facade.create_review(review_data)
        
        place_reviews = self.facade.get_reviews_by_place(place.id)
        
        self.assertEqual(len(place_reviews), 2)
        self.assertTrue(all(review.place.id == place.id for review in place_reviews))

    def test_update_review(self):
        """Test mise à jour d'une review"""
        # Créer les données nécessaires
        user = self.facade.create_user({
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'password123'
        })
        place = self.facade.create_place({
            'title': 'Test Place',
            'description': 'Description',
            'price': 100.0,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'owner_id': user.id
        })
        review_data = {
            'text': 'Original review',
            'rating': 3,
            'user_id': user.id,
            'place_id': place.id
        }
        created_review = self.facade.create_review(review_data)
        
        # Mettre à jour la review
        update_data = {
            'text': 'Updated review',
            'rating': 4
        }
        
        updated_review = self.facade.update_review(created_review.id, update_data)
        
        self.assertIsNotNone(updated_review)
        self.assertEqual(updated_review.text, 'Updated review')
        self.assertEqual(updated_review.rating, 4)

    def test_delete_review(self):
        """Test suppression d'une review"""
        # Créer les données nécessaires
        user = self.facade.create_user({
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'password123'
        })
        place = self.facade.create_place({
            'title': 'Test Place',
            'description': 'Description',
            'price': 100.0,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'owner_id': user.id
        })
        review_data = {
            'text': 'Review to delete',
            'rating': 4,
            'user_id': user.id,
            'place_id': place.id
        }
        created_review = self.facade.create_review(review_data)
        
        # Supprimer la review
        result = self.facade.delete_review(created_review.id)
        self.assertTrue(result)
        
        # Vérifier que la review n'existe plus
        deleted_review = self.facade.get_review(created_review.id)
        self.assertIsNone(deleted_review)

    def test_update_review_invalid_rating(self):
        """Test mise à jour d'une review avec une note invalide"""
        # Créer les données nécessaires
        user = self.facade.create_user({
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'password123'
        })
        place = self.facade.create_place({
            'title': 'Test Place',
            'description': 'Description',
            'price': 100.0,
            'latitude': 48.8566,
            'longitude': 2.3522,
            'owner_id': user.id
        })
        review_data = {
            'text': 'Original review',
            'rating': 4,
            'user_id': user.id,
            'place_id': place.id
        }
        created_review = self.facade.create_review(review_data)
        
        # Essayer de mettre à jour avec une note invalide
        update_data = {
            'rating': 6  # Note invalide
        }
        
        with self.assertRaises(ValueError):
            self.facade.update_review(created_review.id, update_data)


if __name__ == '__main__':
    unittest.main()
