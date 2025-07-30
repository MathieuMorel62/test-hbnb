import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User
from models.place import Place
from models.review import Review


def test_review_creation():
    """Test de la création d'un avis valide"""
    try:
        user = User("Emma", "Jones", "emma.jones@example.com")
        place = Place("Sunny Apartment", "Light and quiet", 75.0, 45.75, 4.85, user)
        review = Review("Great stay!", 5, place, user)

        assert review.text == "Great stay!"
        assert review.rating == 5
        assert review.place == place
        assert review.user == user

        print("✅ Test réussi : création d’un avis valide")

    except Exception as e:
        print("❌ Test échoué :", e)


def test_invalid_rating():
    """Test de la création d'un avis avec une note invalide"""
    try:
        user = User("Liam", "Smith", "liam.smith@example.com")
        place = Place("Tiny House", "", 40.0, 43.6, 1.4, user)
        Review("Pas terrible", 6, place, user)  # Note invalide
        print("❌ Test échoué : note invalide acceptée")
    except ValueError:
        print("✅ Test réussi : note invalide rejetée")


def test_invalid_place_type():
    """Test de la création d'un avis avec un lieu non-valide"""
    try:
        user = User("Noah", "Brown", "noah@example.com")
        Review("Très bon séjour", 4, "pas un lieu", user)
        print("❌ Test échoué : place non-valide acceptée")
    except TypeError:
        print("✅ Test réussi : type de lieu invalide rejeté")


def test_empty_text():
    """Test du texte vide"""
    try:
        user = User("Test", "User", "test@example.com")
        place = Place("Test Place", "desc", 50.0, 45.0, 2.0, user)
        Review("", 4, place, user)  # Texte vide
        print("❌ Test échoué : texte vide accepté")
    except ValueError:
        print("✅ Test réussi : texte vide rejeté")

def test_null_text():
    """Test du texte null"""
    try:
        user = User("Test", "User", "test@example.com")
        place = Place("Test Place", "desc", 50.0, 45.0, 2.0, user)
        Review(None, 4, place, user)  # Texte null
        print("❌ Test échoué : texte null accepté")
    except ValueError:
        print("✅ Test réussi : texte null rejeté")

def test_rating_zero():
    """Test rating = 0 (limite basse invalide)"""
    try:
        user = User("Test", "User", "test@example.com")
        place = Place("Test Place", "desc", 50.0, 45.0, 2.0, user)
        Review("Good", 0, place, user)
        print("❌ Test échoué : rating 0 accepté")
    except ValueError:
        print("✅ Test réussi : rating 0 rejeté")

def test_negative_rating():
    """Test rating négatif"""
    try:
        user = User("Test", "User", "test@example.com")
        place = Place("Test Place", "desc", 50.0, 45.0, 2.0, user)
        Review("Bad", -1, place, user)
        print("❌ Test échoué : rating négatif accepté")
    except ValueError:
        print("✅ Test réussi : rating négatif rejeté")

def test_float_rating():
    """Test rating non-entier"""
    try:
        user = User("Test", "User", "test@example.com")
        place = Place("Test Place", "desc", 50.0, 45.0, 2.0, user)
        Review("Good", 4.5, place, user)  # Float au lieu d'int
        print("❌ Test échoué : rating float accepté")
    except ValueError:
        print("✅ Test réussi : rating float rejeté")

def test_invalid_user_type():
    """Test user invalide"""
    try:
        user = User("Test", "User", "test@example.com")
        place = Place("Test Place", "desc", 50.0, 45.0, 2.0, user)
        Review("Good", 4, place, "pas un user")
        print("❌ Test échoué : user invalide accepté")
    except TypeError:
        print("✅ Test réussi : user invalide rejeté")

def test_inherited_attributes():
    """Test des attributs hérités"""
    try:
        user = User("Test", "User", "test@example.com")
        place = Place("Test Place", "desc", 50.0, 45.0, 2.0, user)
        review = Review("Perfect!", 5, place, user)
        
        assert review.id is not None
        assert review.created_at is not None
        assert review.updated_at is not None
        print("✅ Test réussi : attributs hérités présents")
    except Exception as e:
        print("❌ Test échoué (attributs hérités):", e)


if __name__ == "__main__":
    test_review_creation()
    test_invalid_rating()
    test_invalid_place_type()
    test_empty_text()
    test_null_text()
    test_rating_zero()
    test_negative_rating()
    test_float_rating()
    test_invalid_user_type()
    test_inherited_attributes()
