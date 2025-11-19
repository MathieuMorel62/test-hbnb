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
        # S'assurer que les repositories sont bien stockés dans app.config
        self.app.config['repositories'] = repositories
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Créer un utilisateur propriétaire directement avec la façade
        try:
            owner = facade.create_user({
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "password": "password123"
            })
            self.owner_id = owner.id
            print("Owner created with ID:", self.owner_id)
        except Exception as e:
            print("Error creating owner:", str(e))
            raise

        # Créer un lieu directement avec la façade
        try:
            place = facade.create_place({
                "title": "Bel appartement",
                "description": "Un superbe appartement en centre-ville",
                "price": 100.0,
                "latitude": 48.8566,
                "longitude": 2.3522,
                "owner_id": self.owner_id
            })
            self.place_id = place.id
            print("Place created with ID:", self.place_id)
        except Exception as e:
            print("Error creating place:", str(e))
            raise
        
        # Créer un deuxième utilisateur (non propriétaire) pour les reviews
        try:
            reviewer = facade.create_user({
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane.smith@example.com",
                "password": "password123"
            })
            self.user_id = reviewer.id
            print("Reviewer created with ID:", self.user_id)
        except Exception as e:
            print("Error creating reviewer:", str(e))
            raise
        
        # Obtenir un token JWT pour le reviewer
        self.token = self.get_auth_token('jane.smith@example.com', 'password123')
    
    def get_auth_token(self, email='jane.smith@example.com', password='password123'):
        """Helper pour obtenir un token JWT"""
        # Utiliser la même instance de facade que celle utilisée dans setUp
        login_data = {'email': email, 'password': password}
        response = self.client.post('/api/v1/auth/login',
                                   data=json.dumps(login_data),
                                   content_type='application/json')
        if response.status_code == 200:
            return json.loads(response.data)['access_token']
        # Si le login échoue, peut-être que l'utilisateur n'existe pas encore
        # Dans ce cas, l'utilisateur devrait déjà exister car créé dans setUp
        return None


    def tearDown(self):
        """Nettoyage après chaque test"""
        # Réinitialiser la facade pour éviter les problèmes de partage d'état
        from app.services import facade
        facade._facade = None
        self.app_context.pop()

    def test_create_review(self):
        """Test de la création d'une review"""
        review_data = {
            "text": "Superbe endroit !",
            "rating": 5,
            "place_id": self.place_id
        }
        # user_id est maintenant extrait du JWT, pas besoin de le mettre dans les données

        # Créer la review avec le token JWT
        response = self.client.post('/api/v1/reviews/', 
                                   json=review_data,
                                   headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIsNotNone(data.get('id'))
        self.assertEqual(data['text'], review_data['text'])
        self.assertEqual(data['rating'], review_data['rating'])
        self.assertEqual(data['user_id'], self.user_id)  # Vérifie que user_id est bien celui du token
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
            "place_id": self.place_id
        }
        create_response = self.client.post('/api/v1/reviews/', 
                                           json=review_data,
                                           headers={'Authorization': f'Bearer {self.token}'})
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
            "place_id": self.place_id
        }
        create_response = self.client.post('/api/v1/reviews/', 
                                          json=review_data,
                                          headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(create_response.status_code, 201)
        created_data = create_response.get_json()
        review_id = created_data['id']

        # Mettre à jour la review
        update_data = {
            "text": "Excellent séjour finalement !",
            "rating": 5
        }
        response = self.client.put(f'/api/v1/reviews/{review_id}', 
                                  json=update_data,
                                  headers={'Authorization': f'Bearer {self.token}'})
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
            "place_id": self.place_id
        }
        create_response = self.client.post('/api/v1/reviews/', 
                                          json=review_data,
                                          headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(create_response.status_code, 201)
        created_data = create_response.get_json()
        review_id = created_data['id']

        # Supprimer la review
        response = self.client.delete(f'/api/v1/reviews/{review_id}',
                                     headers={'Authorization': f'Bearer {self.token}'})
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
            "place_id": self.place_id
        }
        review_data2 = {
            "text": "Review 2",
            "rating": 5,
            "place_id": self.place_id
        }
        response1 = self.client.post('/api/v1/reviews/', 
                                    json=review_data1,
                                    headers={'Authorization': f'Bearer {self.token}'})
        # Note: on ne peut créer qu'une seule review par utilisateur et par lieu
        # Pour créer une deuxième review, il faudrait un autre utilisateur
        self.assertEqual(response1.status_code, 201)

        # Récupérer les reviews du lieu
        response = self.client.get(f'/api/v1/reviews/places/{self.place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_create_review_invalid_rating(self):
        """Test de la création d'une review avec une note invalide"""
        review_data = {
            "text": "Test invalide",
            "rating": 6,  # Note invalide
            "place_id": self.place_id
        }
        response = self.client.post('/api/v1/reviews/', 
                                    json=review_data,
                                    headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_place(self):
        """Test de la création d'une review avec un lieu invalide"""
        review_data = {
            "text": "Test invalide",
            "rating": 5,
            "place_id": "invalid_place_id"
        }
        response = self.client.post('/api/v1/reviews/', 
                                   json=review_data,
                                   headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 404)  # Place not found
    
    def test_create_review_own_place(self):
        """Test qu'on ne peut pas créer une review pour son propre lieu"""
        # Vérifier que le lieu existe et obtenir son propriétaire
        place = facade.get_place(self.place_id)
        self.assertIsNotNone(place, "Place should exist")
        self.assertEqual(str(place.owner.id), str(self.owner_id), "Place owner should match owner_id")
        
        # Obtenir un token pour le propriétaire (utiliser l'email du propriétaire créé dans setUp)
        owner_token = self.get_auth_token('john.doe@example.com', 'password123')
        self.assertIsNotNone(owner_token, "Token should be obtained for owner")
        
        # Vérifier que le token contient bien l'ID du propriétaire
        import jwt
        decoded = jwt.decode(owner_token, self.app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        token_user_id = decoded['sub']
        self.assertEqual(str(token_user_id), str(self.owner_id), f"Token user ID ({token_user_id}) should match owner_id ({self.owner_id})")
        
        review_data = {
            "text": "Test invalide",
            "rating": 5,
            "place_id": self.place_id
        }
        response = self.client.post('/api/v1/reviews/', 
                                   json=review_data,
                                   headers={'Authorization': f'Bearer {owner_token}'})
        # Doit échouer car on ne peut pas review son propre lieu
        self.assertEqual(response.status_code, 400, f"Expected 400, got {response.status_code}. Response: {response.get_json()}")
        data = response.get_json()
        self.assertIn('error', data, f"Response should contain 'error' key. Got: {data}")
        self.assertEqual(data['error'], 'You cannot review your own place')
    
    def test_create_review_duplicate(self):
        """Test qu'on ne peut pas créer plusieurs reviews pour le même lieu"""
        review_data = {
            "text": "Première review",
            "rating": 5,
            "place_id": self.place_id
        }
        response1 = self.client.post('/api/v1/reviews/', 
                                    json=review_data,
                                    headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response1.status_code, 201)
        
        # Essayer de créer une deuxième review pour le même lieu
        review_data2 = {
            "text": "Deuxième review",
            "rating": 4,
            "place_id": self.place_id
        }
        response2 = self.client.post('/api/v1/reviews/', 
                                     json=review_data2,
                                     headers={'Authorization': f'Bearer {self.token}'})
        # Doit échouer car on ne peut créer qu'une seule review par lieu
        self.assertEqual(response2.status_code, 400)
        data = response2.get_json()
        self.assertEqual(data['error'], 'You have already reviewed this place')
    
    def test_update_review_unauthorized(self):
        """Test qu'on ne peut pas modifier une review d'un autre utilisateur"""
        # Créer une review avec le reviewer
        review_data = {
            "text": "Review à modifier",
            "rating": 4,
            "place_id": self.place_id
        }
        create_response = self.client.post('/api/v1/reviews/', 
                                          json=review_data,
                                          headers={'Authorization': f'Bearer {self.token}'})
        review_id = create_response.get_json()['id']
        
        # Créer un autre utilisateur et obtenir son token
        other_user = facade.create_user({
            "first_name": "Other",
            "last_name": "User",
            "email": "other@example.com",
            "password": "password123"
        })
        other_token = self.get_auth_token('other@example.com', 'password123')
        
        # L'autre utilisateur essaie de modifier la review
        update_data = {
            "text": "Hacked review",
            "rating": 1
        }
        response = self.client.put(f'/api/v1/reviews/{review_id}', 
                                  json=update_data,
                                  headers={'Authorization': f'Bearer {other_token}'})
        
        # Doit échouer car ce n'est pas sa review
        self.assertEqual(response.status_code, 403)
        data = response.get_json()
        self.assertEqual(data['error'], 'Unauthorized action')
    
    def test_delete_review_unauthorized(self):
        """Test qu'on ne peut pas supprimer une review d'un autre utilisateur"""
        # Créer une review avec le reviewer
        review_data = {
            "text": "Review à supprimer",
            "rating": 4,
            "place_id": self.place_id
        }
        create_response = self.client.post('/api/v1/reviews/', 
                                          json=review_data,
                                          headers={'Authorization': f'Bearer {self.token}'})
        review_id = create_response.get_json()['id']
        
        # Créer un autre utilisateur et obtenir son token
        other_user = facade.create_user({
            "first_name": "Other",
            "last_name": "User",
            "email": "other2@example.com",
            "password": "password123"
        })
        other_token = self.get_auth_token('other2@example.com', 'password123')
        
        # L'autre utilisateur essaie de supprimer la review
        response = self.client.delete(f'/api/v1/reviews/{review_id}',
                                     headers={'Authorization': f'Bearer {other_token}'})
        
        # Doit échouer car ce n'est pas sa review
        self.assertEqual(response.status_code, 403)
        data = response.get_json()
        self.assertEqual(data['error'], 'Unauthorized action')
    
    def test_create_review_without_token(self):
        """Test qu'on ne peut pas créer une review sans token JWT"""
        review_data = {
            "text": "Test sans token",
            "rating": 5,
            "place_id": self.place_id
        }
        response = self.client.post('/api/v1/reviews/', 
                                   json=review_data)
        # Doit échouer car pas de token
        self.assertEqual(response.status_code, 401)
    
    def test_update_review_without_token(self):
        """Test qu'on ne peut pas modifier une review sans token JWT"""
        # Créer une review d'abord
        review_data = {
            "text": "Review à modifier",
            "rating": 4,
            "place_id": self.place_id
        }
        create_response = self.client.post('/api/v1/reviews/', 
                                          json=review_data,
                                          headers={'Authorization': f'Bearer {self.token}'})
        review_id = create_response.get_json()['id']
        
        # Essayer de modifier sans token
        update_data = {
            "text": "Hacked review",
            "rating": 1
        }
        response = self.client.put(f'/api/v1/reviews/{review_id}', 
                                  json=update_data)
        
        # Doit échouer car pas de token
        self.assertEqual(response.status_code, 401)
    
    def test_delete_review_without_token(self):
        """Test qu'on ne peut pas supprimer une review sans token JWT"""
        # Créer une review d'abord
        review_data = {
            "text": "Review à supprimer",
            "rating": 4,
            "place_id": self.place_id
        }
        create_response = self.client.post('/api/v1/reviews/', 
                                          json=review_data,
                                          headers={'Authorization': f'Bearer {self.token}'})
        review_id = create_response.get_json()['id']
        
        # Essayer de supprimer sans token
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        
        # Doit échouer car pas de token
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
