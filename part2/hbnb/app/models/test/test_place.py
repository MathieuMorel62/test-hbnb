import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class TestPlace(unittest.TestCase):
    """Tests unitaires pour la classe Place"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.user = User("Alice", "Smith", "alice@example.com")

    def test_place_creation(self):
        """Test de la création d'un lieu valide"""
        place = Place(
            title="Cozy Loft",
            description="A lovely spot in the city center",
            price=89.99,
            latitude=48.8566,
            longitude=2.3522,
            owner=self.user
        )

        self.assertEqual(place.title, "Cozy Loft")
        self.assertEqual(place.description, "A lovely spot in the city center")
        self.assertEqual(place.price, 89.99)
        self.assertEqual(place.latitude, 48.8566)
        self.assertEqual(place.longitude, 2.3522)
        self.assertEqual(place.owner, self.user)
        self.assertEqual(place.reviews, [])
        self.assertEqual(place.amenities, [])

    def test_empty_title(self):
        """Test titre vide"""
        with self.assertRaises(ValueError):
            Place("", "Description", 100.0, 45.0, 2.0, self.user)

    def test_long_title(self):
        """Test titre trop long"""
        with self.assertRaises(ValueError):
            Place("A" * 101, "Description", 100.0, 45.0, 2.0, self.user)

    def test_negative_price(self):
        """Test prix négatif"""
        with self.assertRaises(ValueError):
            Place("Test", "Description", -50.0, 45.0, 2.0, self.user)

    def test_zero_price(self):
        """Test prix zéro"""
        with self.assertRaises(ValueError):
            Place("Test", "Description", 0.0, 45.0, 2.0, self.user)

    def test_invalid_latitude(self):
        """Test latitude invalide"""
        with self.assertRaises(ValueError):
            Place("Test", "Description", 100.0, 95.0, 2.0, self.user)

    def test_invalid_longitude(self):
        """Test longitude invalide"""
        with self.assertRaises(ValueError):
            Place("Test", "Description", 100.0, 45.0, 190.0, self.user)

    def test_invalid_owner(self):
        """Test de l'ajout d'un propriétaire invalide"""
        with self.assertRaises(TypeError):
            Place("Test", "Description", 100.0, 45.0, 2.0, "not_a_user")

    def test_add_review(self):
        """Test de l'ajout d'une review à un lieu"""
        place = Place("Charming Flat", "", 120.0, 45.0, 3.0, self.user)
        review = Review("Great stay!", 5, place, self.user)

        place.add_review(review)

        self.assertEqual(len(place.reviews), 1)
        self.assertEqual(place.reviews[0].text, "Great stay!")

    def test_add_amenity(self):
        """Test de l'ajout d'une amenity à un lieu"""
        place = Place("Seaside House", "Ocean view", 150.0, 43.0, -1.0, self.user)
        amenity = Amenity("Wi-Fi")

        place.add_amenity(amenity)

        self.assertEqual(len(place.amenities), 1)
        self.assertEqual(place.amenities[0].name, "Wi-Fi")


if __name__ == "__main__":
    unittest.main()
