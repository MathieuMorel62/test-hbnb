import sys
import os

# Ajout du chemin du projet à sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User


def test_user_creation():
    """Test de la création d'un utilisateur valide"""
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


def test_invalid_email():
    """Test de la création d'un utilisateur avec un email invalide"""
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


def test_long_first_name():
    """Test de la création d'un utilisateur avec un prénom trop long"""
    try:
        User(
            first_name="A" * 51,
            last_name="Martin",
            email="bob@example.com"
        )
        print("❌ Test échoué : prénom trop long accepté")
    except ValueError as e:
        print("✅ Test réussi : prénom trop long rejeté")


def test_long_last_name():
    """Test de la création d'un utilisateur avec un nom trop long"""
    try:
        User(
            first_name="Bob",
            last_name="M" * 51,
            email="bob@example.com"
        )
        print("❌ Test échoué : nom trop long accepté")
    except ValueError as e:
        print("✅ Test réussi : nom trop long rejeté")


def test_empty_first_name():
    """Test first_name vide"""
    try:
        User(first_name="", last_name="Dupont", email="test@example.com")
        print("❌ Test échoué : first_name vide accepté")
    except ValueError:
        print("✅ Test réussi : first_name vide rejeté")


def test_empty_last_name():
    """Test last_name vide"""
    try:
        User(first_name="Alice", last_name="", email="test@example.com")
        print("❌ Test échoué : last_name vide accepté")
    except ValueError:
        print("✅ Test réussi : last_name vide rejeté")


def test_user_admin():
    """Test utilisateur admin"""
    try:
        user = User("Alice", "Dupont", "alice@example.com", is_admin=True)
        assert user.is_admin is True
        print("✅ Test réussi : utilisateur admin créé")
    except Exception as e:
        print("❌ Test échoué :", e)


def test_user_update():
    """Test mise à jour utilisateur"""
    try:
        user = User("Alice", "Dupont", "alice@example.com")
        old_updated_at = user.updated_at
        
        # Petite pause pour s'assurer que le timestamp change
        import time
        time.sleep(0.001)
        
        user.update({"first_name": "Alicia"})
        assert user.first_name == "Alicia"
        assert user.updated_at > old_updated_at
        print("✅ Test réussi : mise à jour utilisateur")
    except Exception as e:
        print("❌ Test échoué :", e)


def test_max_length_valid():
    """Test longueurs maximales valides (50 caractères)"""
    try:
        user = User(
            first_name="A" * 50,
            last_name="B" * 50,
            email="test@example.com"
        )
        assert len(user.first_name) == 50
        assert len(user.last_name) == 50
        print("✅ Test réussi : longueurs maximales valides")
    except Exception as e:
        print("❌ Test échoué :", e)


def test_email_edge_cases():
    """Tests d'emails spécifiques"""
    valid_emails = [
        "user@domain.com",
        "user.name@domain.co.uk", 
        "user+tag@domain.org"
    ]
    invalid_emails = [
        "",           # vide
        "user@",      # pas de domaine
        "@domain.com", # pas de partie locale  
        "user.domain.com" # pas de @
    ]
    for email in valid_emails:
        try:
            User(first_name="Test", last_name="User", email=email)
            print(f"✅ Test réussi : email valide - {email}")
        except ValueError:
            print(f"❌ Test échoué : email invalide - {email}")
    for email in invalid_emails:
        try:
            User(first_name="Test", last_name="User", email=email)
            print(f"❌ Test échoué : email valide - {email}")
        except ValueError:
            print(f"✅ Test réussi : email invalide - {email}")
        
        
if __name__ == "__main__":
    test_user_creation()
    test_invalid_email()
    test_long_first_name()
    test_long_last_name()
    test_empty_first_name()
    test_empty_last_name()
    test_user_admin()
    test_user_update()
    test_max_length_valid()
    test_email_edge_cases()
