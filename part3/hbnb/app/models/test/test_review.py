import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from app.models.user import User
from app.models.place import Place
from app.models.review import Review


class TestReview(unittest.TestCase):
    """Tests unitaires pour la classe Review"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.user = User("Emma", "Jones", "emma.jones@example.com")
        self.place = Place("Sunny Apartment", "Light and quiet", 75.0, 45.75, 4.85, self.user)

    def test_review_creation(self):
        """Test de la création d'un avis valide"""
        review = Review("Great stay!", 5, self.place, self.user)

        self.assertEqual(review.text, "Great stay!")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.place, self.place)
        self.assertEqual(review.user, self.user)

    def test_invalid_rating(self):
        """Test de la création d'un avis avec une note invalide"""
        with self.assertRaises(ValueError):
            Review("Pas terrible", 6, self.place, self.user)

    def test_rating_zero(self):
        """Test rating = 0 (limite basse invalide)"""
        with self.assertRaises(ValueError):
            Review("Good", 0, self.place, self.user)

    def test_negative_rating(self):
        """Test rating négatif"""
        with self.assertRaises(ValueError):
            Review("Bad", -1, self.place, self.user)

    def test_float_rating(self):
        """Test rating non-entier"""
        with self.assertRaises(ValueError):
            Review("Good", 4.5, self.place, self.user)

    def test_invalid_place_type(self):
        """Test de la création d'un avis avec un lieu non-valide"""
        with self.assertRaises(TypeError):
            Review("Très bon séjour", 4, "pas un lieu", self.user)

    def test_invalid_user_type(self):
        """Test user invalide"""
        with self.assertRaises(TypeError):
            Review("Good", 4, self.place, "pas un user")

    def test_empty_text(self):
        """Test du texte vide"""
        with self.assertRaises(ValueError):
            Review("", 4, self.place, self.user)

    def test_null_text(self):
        """Test du texte null"""
        with self.assertRaises(ValueError):
            Review(None, 4, self.place, self.user)

    def test_inherited_attributes(self):
        """Test des attributs hérités"""
        review = Review("Perfect!", 5, self.place, self.user)
        
        self.assertIsNotNone(review.id)
        self.assertIsNotNone(review.created_at)
        self.assertIsNotNone(review.updated_at)


if __name__ == "__main__":
    unittest.main()
