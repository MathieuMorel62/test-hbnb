import sys
import os
import unittest
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """Tests unitaires pour la classe Amenity"""

    def test_amenity_creation(self):
        """Test de la création d'un équipement valide"""
        amenity = Amenity("Wi-Fi")
        self.assertEqual(amenity.name, "Wi-Fi")
        self.assertIsNotNone(amenity.id)

    def test_invalid_name(self):
        """Test de la création d'un équipement avec un nom trop long"""
        with self.assertRaises(ValueError):
            Amenity("A" * 51)

    def test_empty_name(self):
        """Test nom vide"""
        with self.assertRaises(ValueError):
            Amenity("")

    def test_none_name(self):
        """Test nom None"""
        with self.assertRaises(ValueError):
            Amenity(None)

    def test_whitespace_name(self):
        """Test nom avec espaces"""
        with self.assertRaises(ValueError):
            Amenity("   ")

    def test_valid_edge_cases(self):
        """Test cas limites valides"""
        amenity_50 = Amenity("A" * 50)
        self.assertEqual(len(amenity_50.name), 50)
        
        amenity_1 = Amenity("A")
        self.assertEqual(amenity_1.name, "A")

    def test_base_model_attributes(self):
        """Test attributs BaseModel présents"""
        amenity = Amenity("Parking")

        self.assertIsNotNone(amenity.id)
        self.assertIsNotNone(amenity.created_at)
        self.assertIsNotNone(amenity.updated_at)
        self.assertEqual(len(amenity.id), 36)  # UUID format

    def test_save_and_update_methods(self):
        """Test méthodes save() et update()"""
        amenity = Amenity("Pool")
        original_updated_at = amenity.updated_at
        
        time.sleep(0.01)
        amenity.save()
        self.assertGreater(amenity.updated_at, original_updated_at)

        amenity.update({"name": "Swimming Pool"})
        self.assertEqual(amenity.name, "Swimming Pool")


if __name__ == "__main__":
    unittest.main()