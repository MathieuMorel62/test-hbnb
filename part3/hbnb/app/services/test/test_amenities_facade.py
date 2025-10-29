import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from app.services.facade import HBnBFacade
from app.models.amenity import Amenity


class TestAmenitiesFacade(unittest.TestCase):
    """Tests pour la facade amenities"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.facade = HBnBFacade()

    def test_create_amenity(self):
        """Test création d'amenity via facade"""
        amenity_data = {'name': 'Wi-Fi'}
        
        amenity = self.facade.create_amenity(amenity_data)
        
        self.assertIsInstance(amenity, Amenity)
        self.assertEqual(amenity.name, 'Wi-Fi')
        self.assertIsNotNone(amenity.id)

    def test_get_amenity(self):
        """Test récupération d'amenity par ID"""
        amenity_data = {'name': 'Pool'}
        
        created_amenity = self.facade.create_amenity(amenity_data)
        retrieved_amenity = self.facade.get_amenity(created_amenity.id)
        
        self.assertIsNotNone(retrieved_amenity)
        self.assertEqual(retrieved_amenity.id, created_amenity.id)
        self.assertEqual(retrieved_amenity.name, 'Pool')

    def test_get_amenity_not_found(self):
        """Test récupération d'amenity inexistante"""
        amenity = self.facade.get_amenity('nonexistent-id')
        self.assertIsNone(amenity)

    def test_get_all_amenities(self):
        """Test récupération de toutes les amenities"""
        amenities_data = [
            {'name': 'Wi-Fi'},
            {'name': 'Air Conditioning'}
        ]
        
        for amenity_data in amenities_data:
            self.facade.create_amenity(amenity_data)
        
        all_amenities = self.facade.get_all_amenities()
        
        self.assertEqual(len(all_amenities), 2)
        self.assertIsInstance(all_amenities[0], Amenity)
        self.assertIsInstance(all_amenities[1], Amenity)

    def test_update_amenity_success(self):
        """Test mise à jour d'amenity avec succès"""
        amenity_data = {'name': 'Original Name'}
        
        created_amenity = self.facade.create_amenity(amenity_data)
        
        update_data = {'name': 'Updated Name'}
        updated_amenity = self.facade.update_amenity(created_amenity.id, update_data)
        
        self.assertIsNotNone(updated_amenity)
        self.assertEqual(updated_amenity.name, 'Updated Name')

    def test_update_amenity_not_found(self):
        """Test mise à jour d'amenity inexistante"""
        update_data = {'name': 'Updated'}
        updated_amenity = self.facade.update_amenity('nonexistent-id', update_data)
        self.assertIsNone(updated_amenity)

    def test_update_amenity_invalid_data_facade(self):
        """Test mise à jour d'amenity avec données invalides dans la facade"""
        amenity_data = {'name': 'Original Name'}
        
        created_amenity = self.facade.create_amenity(amenity_data)
        
        # Essayer de mettre à jour avec nom vide
        update_data = {'name': ''}
        
        with self.assertRaises(ValueError) as context:
            self.facade.update_amenity(created_amenity.id, update_data)
        
        self.assertEqual(str(context.exception), "The name of the equipment is required and must be less than 50 characters.")

    def test_update_amenity_long_name_facade(self):
        """Test mise à jour d'amenity avec nom trop long dans la facade"""
        amenity_data = {'name': 'Original Name'}
        
        created_amenity = self.facade.create_amenity(amenity_data)
        
        # Essayer de mettre à jour avec nom trop long
        update_data = {'name': 'A' * 51}
        
        with self.assertRaises(ValueError) as context:
            self.facade.update_amenity(created_amenity.id, update_data)
        
        self.assertEqual(str(context.exception), "The name of the equipment is required and must be less than 50 characters.")

    def test_create_amenity_invalid_name(self):
        """Test création d'amenity avec nom invalide"""
        # Test avec nom vide
        amenity_data = {'name': ''}
        
        with self.assertRaises(ValueError) as context:
            self.facade.create_amenity(amenity_data)
        
        self.assertEqual(str(context.exception), "The name of the equipment is required and must be less than 50 characters.")

    def test_create_amenity_long_name(self):
        """Test création d'amenity avec nom trop long"""
        # Test avec nom trop long
        amenity_data = {'name': 'A' * 51}
        
        with self.assertRaises(ValueError) as context:
            self.facade.create_amenity(amenity_data)
        
        self.assertEqual(str(context.exception), "The name of the equipment is required and must be less than 50 characters.")


if __name__ == '__main__':
    unittest.main()
