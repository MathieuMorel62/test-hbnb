import sys
import os
import unittest
import json
from flask import Flask
from flask_restx import Api

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from app import create_app
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.services import facade
from app.services.facade import HBnBFacade
from app.persistence.repository import InMemoryRepository


class TestReviewsEndpoints(unittest.TestCase):
    """Tests unitaires pour les endpoints des reviews"""

    def setUp(self):
        """Configuration avant chaque test"""
        # Créer des repositories partagés pour les tests
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        
        # Créer les repositories pour l'application
        repositories = {
            'user_repo': self.user_repo,
            'place_repo': self.place_repo,
            'review_repo': self.review_repo,
            'amenity_repo': self.amenity_repo
        }
        
        # Créer l'application avec les repositories
        self.app = create_app(repositories)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Créer un utilisateur directement avec la façade
        try:
            user = facade.create_user({
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com"
            })
            self.user_id = user.id
            print("User created with ID:", self.user_id)
        except Exception as e:
            print("Error creating user:", str(e))
            raise

        # Créer un lieu directement avec la façade
        try:
            place = facade.create_place({
                "title": "Bel appartement",
                "description": "Un superbe appartement en centre-ville",
                "price": 100.0,
                "latitude": 48.8566,
                "longitude": 2.3522,
                "owner_id": self.user_id
            })
            self.place_id = place.id
            print("Place created with ID:", self.place_id)
        except Exception as e:
            print("Error creating place:", str(e))
            raise


    def tearDown(self):
        """Nettoyage après chaque test"""
        self.app_context.pop()

    def test_create_review(self):
        """Test de la création d'une review"""
        review_data = {
            "text": "Superbe endroit !",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
        # Vérifier que le lieu existe
        place = facade.get_place(self.place_id)
        print("Place exists:", place is not None)
        if place:
            print("Place ID:", place.id)
            print("Place title:", place.title)

        # Vérifier que l'utilisateur existe
        user = facade.get_user(self.user_id)
        print("User exists:", user is not None)
        if user:
            print("User ID:", user.id)
            print("User email:", user.email)

        # Créer la review
        response = self.client.post('/api/v1/reviews/', json=review_data)
        print("Review data:", review_data)
        print("Response:", response.get_json())
        print("Status code:", response.status_code)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIsNotNone(data.get('id'))
        self.assertEqual(data['text'], review_data['text'])
        self.assertEqual(data['rating'], review_data['rating'])
        self.assertEqual(data['user_id'], self.user_id)
        self.assertEqual(data['place_id'], self.place_id)

    def test_get_all_reviews(self):
        """Test de la récupération de toutes les reviews"""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_review(self):
        """Test de la récupération d'une review spécifique"""
        # Créer une review
        review_data = {
            "text": "Excellent séjour !",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
        create_response = self.client.post('/api/v1/reviews/', json=review_data)
        self.assertEqual(create_response.status_code, 201)
        created_data = create_response.get_json()
        review_id = created_data['id']

        # Récupérer la review
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['text'], review_data['text'])
        self.assertEqual(data['rating'], review_data['rating'])

    def test_update_review(self):
        """Test de la mise à jour d'une review"""
        # Créer une review
        review_data = {
            "text": "Bon séjour",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
        create_response = self.client.post('/api/v1/reviews/', json=review_data)
        self.assertEqual(create_response.status_code, 201)
        created_data = create_response.get_json()
        review_id = created_data['id']

        # Mettre à jour la review
        update_data = {
            "text": "Excellent séjour finalement !",
            "rating": 5
        }
        response = self.client.put(f'/api/v1/reviews/{review_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()['review']
        self.assertEqual(data['text'], update_data['text'])
        self.assertEqual(data['rating'], update_data['rating'])

    def test_delete_review(self):
        """Test de la suppression d'une review"""
        # Créer une review
        review_data = {
            "text": "À supprimer",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
        create_response = self.client.post('/api/v1/reviews/', json=review_data)
        self.assertEqual(create_response.status_code, 201)
        created_data = create_response.get_json()
        review_id = created_data['id']

        # Supprimer la review
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

        # Vérifier que la review n'existe plus
        get_response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 404)

    def test_get_place_reviews(self):
        """Test de la récupération des reviews d'un lieu"""
        # Créer quelques reviews pour le lieu
        review_data1 = {
            "text": "Review 1",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
        review_data2 = {
            "text": "Review 2",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
        response1 = self.client.post('/api/v1/reviews/', json=review_data1)
        response2 = self.client.post('/api/v1/reviews/', json=review_data2)
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 201)

        # Récupérer les reviews du lieu
        response = self.client.get(f'/api/v1/reviews/places/{self.place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 2)

    def test_create_review_invalid_rating(self):
        """Test de la création d'une review avec une note invalide"""
        review_data = {
            "text": "Test invalide",
            "rating": 6,  # Note invalide
            "user_id": self.user_id,
            "place_id": self.place_id
        }
        response = self.client.post('/api/v1/reviews/', json=review_data)
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_user(self):
        """Test de la création d'une review avec un utilisateur invalide"""
        review_data = {
            "text": "Test invalide",
            "rating": 5,
            "user_id": "invalid_user_id",
            "place_id": self.place_id
        }
        response = self.client.post('/api/v1/reviews/', json=review_data)
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_place(self):
        """Test de la création d'une review avec un lieu invalide"""
        review_data = {
            "text": "Test invalide",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": "invalid_place_id"
        }
        response = self.client.post('/api/v1/reviews/', json=review_data)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
