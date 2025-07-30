import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


def test_place_creation():
    """Test de la création d'un lieu valide"""
    try:
        user = User("Alice", "Smith", "alice@example.com")
        place = Place(
            title="Cozy Loft",
            description="A lovely spot in the city center",
            price=89.99,
            latitude=48.8566,
            longitude=2.3522,
            owner=user
        )

        assert place.title == "Cozy Loft"
        assert place.description == "A lovely spot in the city center"
        assert place.price == 89.99
        assert place.latitude == 48.8566
        assert place.longitude == 2.3522
        assert place.owner == user
        assert place.reviews == []
        assert place.amenities == []

        print("✅ Test réussi : création d’un lieu valide")

    except Exception as e:
        print("❌ Test échoué (creation):", e)

    
def test_empty_title():
    """Test titre vide"""
    try:
        user = User("John", "Doe", "john@example.com")
        Place("", "Description", 100.0, 45.0, 2.0, user)
        print("❌ Test échoué : titre vide accepté")
    except ValueError:
        print("✅ Test réussi : titre vide rejeté")


def test_long_title():
    """Test titre trop long"""
    try:
        user = User("John", "Doe", "john@example.com")
        Place("A" * 101, "Description", 100.0, 45.0, 2.0, user)
        print("❌ Test échoué : titre trop long accepté")
    except ValueError:
        print("✅ Test réussi : titre trop long rejeté")


def test_negative_price():
    """Test prix négatif"""
    try:
        user = User("John", "Doe", "john@example.com")
        Place("Test", "Description", -50.0, 45.0, 2.0, user)
        print("❌ Test échoué : prix négatif accepté")
    except ValueError:
        print("✅ Test réussi : prix négatif rejeté")


def test_zero_price():
    """Test prix zéro"""
    try:
        user = User("John", "Doe", "john@example.com")
        Place("Test", "Description", 0.0, 45.0, 2.0, user)
        print("❌ Test échoué : prix zéro accepté")
    except ValueError:
        print("✅ Test réussi : prix zéro rejeté")


def test_add_review():
    """Test de l'ajout d'une review à un lieu"""
    try:
        user = User("Bob", "Martin", "bob@example.com")
        place = Place("Charming Flat", "", 120.0, 45.0, 3.0, user)
        review = Review("Great stay!", 5, place, user)

        place.add_review(review)

        assert len(place.reviews) == 1
        assert place.reviews[0].text == "Great stay!"

        print("✅ Test réussi : ajout d’un avis à un lieu")

    except Exception as e:
        print("❌ Test échoué (review):", e)


def test_invalid_latitude():
    """Test latitude invalide"""
    try:
        user = User("John", "Doe", "john@example.com")
        Place("Test", "Description", 100.0, 95.0, 2.0, user)
        print("❌ Test échoué : latitude invalide acceptée")
    except ValueError:
        print("✅ Test réussi : latitude invalide rejetée")


def test_invalid_longitude():
    """Test longitude invalide"""
    try:
        user = User("John", "Doe", "john@example.com")
        Place("Test", "Description", 100.0, 45.0, 190.0, user)
        print("❌ Test échoué : longitude invalide acceptée")
    except ValueError:
        print("✅ Test réussi : longitude invalide rejetée")


def test_add_amenity():
    """Test de l'ajout d'une amenity à un lieu"""
    try:
        user = User("Charlie", "Doe", "charlie@example.com")
        place = Place("Seaside House", "Ocean view", 150.0, 43.0, -1.0, user)
        amenity = Amenity("Wi-Fi")

        place.add_amenity(amenity)

        assert len(place.amenities) == 1
        assert place.amenities[0].name == "Wi-Fi"

        print("✅ Test réussi : ajout d’un équipement à un lieu")

    except Exception as e:
        print("❌ Test échoué (amenity):", e)


def test_invalid_owner():
    """Test de l'ajout d'un propriétaire invalide"""
    try:
        Place("Test", "Description", 100.0, 45.0, 2.0, "not_a_user")
        print("❌ Test échoué : propriétaire invalide accepté")
    except TypeError:
        print("✅ Test réussi : propriétaire invalide rejeté")


if __name__ == "__main__":
    test_place_creation()
    test_add_review()
    test_add_amenity()
    test_empty_title()
    test_long_title()
    test_negative_price()
    test_zero_price()
    test_invalid_latitude()
    test_invalid_longitude()
    test_invalid_owner()
