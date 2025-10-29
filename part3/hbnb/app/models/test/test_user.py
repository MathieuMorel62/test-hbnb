import sys
import os
import unittest
import time

# Ajout du chemin du projet à sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from app.models.user import User


class TestUser(unittest.TestCase):
    """Tests unitaires pour la classe User"""

    def test_user_creation(self):
        """Test de la création d'un utilisateur valide"""
        user = User(
            first_name="Alice",
            last_name="Dupont",
            email="alice.dupont@example.com"
        )
        self.assertEqual(user.first_name, "Alice")
        self.assertEqual(user.last_name, "Dupont")
        self.assertEqual(user.email, "alice.dupont@example.com")
        self.assertFalse(user.is_admin)
        self.assertIsNotNone(user.id)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)

    def test_invalid_email(self):
        """Test de la création d'un utilisateur avec un email invalide"""
        with self.assertRaises(ValueError):
            User(
                first_name="Bob",
                last_name="Martin",
                email="adresse_invalide"
            )

    def test_long_first_name(self):
        """Test de la création d'un utilisateur avec un prénom trop long"""
        with self.assertRaises(ValueError):
            User(
                first_name="A" * 51,
                last_name="Martin",
                email="bob@example.com"
            )

    def test_long_last_name(self):
        """Test de la création d'un utilisateur avec un nom trop long"""
        with self.assertRaises(ValueError):
            User(
                first_name="Bob",
                last_name="M" * 51,
                email="bob@example.com"
            )

    def test_empty_first_name(self):
        """Test first_name vide"""
        with self.assertRaises(ValueError):
            User(first_name="", last_name="Dupont", email="test@example.com")

    def test_empty_last_name(self):
        """Test last_name vide"""
        with self.assertRaises(ValueError):
            User(first_name="Alice", last_name="", email="test@example.com")

    def test_user_admin(self):
        """Test utilisateur admin"""
        user = User("Alice", "Dupont", "alice@example.com", is_admin=True)
        self.assertTrue(user.is_admin)

    def test_user_update(self):
        """Test mise à jour utilisateur"""
        user = User("Alice", "Dupont", "alice@example.com")
        old_updated_at = user.updated_at
        
        # Petite pause pour s'assurer que le timestamp change
        time.sleep(0.001)
        
        user.update({"first_name": "Alicia"})
        self.assertEqual(user.first_name, "Alicia")
        self.assertGreater(user.updated_at, old_updated_at)

    def test_max_length_valid(self):
        """Test longueurs maximales valides (50 caractères)"""
        user = User(
            first_name="A" * 50,
            last_name="B" * 50,
            email="test@example.com"
        )
        self.assertEqual(len(user.first_name), 50)
        self.assertEqual(len(user.last_name), 50)

    def test_valid_emails(self):
        """Tests d'emails valides"""
        valid_emails = [
            "user@domain.com",
            "user.name@domain.co.uk", 
            "user+tag@domain.org"
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                user = User(first_name="Test", last_name="User", email=email)
                self.assertEqual(user.email, email)

    def test_invalid_emails(self):
        """Tests d'emails invalides"""
        invalid_emails = [
            "",           # vide
            "user@",      # pas de domaine
            "@domain.com", # pas de partie locale  
            "user.domain.com" # pas de @
        ]
        for email in invalid_emails:
            with self.subTest(email=email):
                with self.assertRaises(ValueError):
                    User(first_name="Test", last_name="User", email=email)


if __name__ == "__main__":
    unittest.main()
