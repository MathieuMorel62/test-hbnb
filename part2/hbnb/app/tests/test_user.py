import sys
import os

# Ajout du chemin du projet à sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User

# Test de la création d'un utilisateur valide
def test_user_creation():
    try:
        user = User(
            first_name="Alice",
            last_name="Dupont",
            email="alice.dupont@example.com"
        )
        assert user.first_name == "Alice"
        assert user.last_name == "Dupont"
        assert user.email == "alice.dupont@example.com"
        assert user.is_admin is False
        assert user.id is not None
        assert user.created_at is not None
        assert user.updated_at is not None

        print("✅ Test réussi : création d’un utilisateur valide")

    except Exception as e:
        print("❌ Test échoué :", e)

# Test de la création d'un utilisateur avec un email invalide
def test_invalid_email():
    try:
        User(
            first_name="Bob",
            last_name="Martin",
            email="adresse_invalide"
        )
        print("❌ Test échoué : email invalide accepté")
    except ValueError as e:
        print("✅ Test réussi : email invalide rejeté")
    except Exception as e:
        print("❌ Test échoué :", e)


# Test de la création d'un utilisateur avec un prénom trop long
def test_long_first_name():
    try:
        User(
            first_name="A" * 51,
            last_name="Martin",
            email="bob@example.com"
        )
        print("❌ Test échoué : prénom trop long accepté")
    except ValueError as e:
        print("✅ Test réussi : prénom trop long rejeté")

# Test de la création d'un utilisateur avec un nom trop long
def test_long_last_name():
    try:
        User(
            first_name="Bob",
            last_name="M" * 51,
            email="bob@example.com"
        )
        print("❌ Test échoué : nom trop long accepté")
    except ValueError as e:
        print("✅ Test réussi : nom trop long rejeté")
        

if __name__ == "__main__":
    test_user_creation()
    test_invalid_email()
    test_long_first_name()
    test_long_last_name()
