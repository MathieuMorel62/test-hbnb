import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.amenity import Amenity


def test_amenity_creation():
    """Test de la création d'un équipement valide"""
    try:
        amenity = Amenity("Wi-Fi")
        assert amenity.name == "Wi-Fi"
        assert amenity.id is not None
        print("✅ Test réussi : création d’un équipement valide")
    except Exception as e:
        print("❌ Test échoué :", e)


def test_invalid_name():
    """Test de la création d'un équipement avec un nom trop long"""
    try:
        Amenity("A" * 51)
        print("❌ Test échoué : nom trop long accepté")
    except ValueError:
        print("✅ Test réussi : nom trop long rejeté")


def test_empty_name():
    """Test nom vide"""
    try:
        Amenity("") 
        print("❌ Test échoué : nom vide accepté")
    except ValueError:
        print("✅ Test réussi : nom vide rejeté")


def test_none_name():
    """Test nom None"""
    try:
        Amenity(None)
        print("❌ Test échoué : nom None accepté") 
    except ValueError:
        print("✅ Test réussi : nom None rejeté")


def test_whitespace_name():
    """Test nom avec espaces"""
    try:
        Amenity("   ")  # Espaces seulement
        print("❌ Test échoué : nom avec espaces accepté")
    except ValueError:
        print("✅ Test réussi : nom avec espaces rejeté")


def test_valid_edge_cases():
    """Test cas limites valides"""
    try:
        amenity_50 = Amenity("A" * 50)
        assert len(amenity_50.name) == 50
        
        amenity_1 = Amenity("A")
        assert amenity_1.name == "A"
        
        print("✅ Test réussi : cas limites valides")
    except Exception as e:
        print("❌ Test échoué :", e)


def test_base_model_attributes():
    """Test attributs BaseModel présents"""
    try:
        amenity = Amenity("Parking")

        assert amenity.id is not None
        assert amenity.created_at is not None
        assert amenity.updated_at is not None
        assert len(amenity.id) == 36  # UUID format
        
        print("✅ Test réussi : attributs BaseModel présents")
    except Exception as e:
        print("❌ Test échoué :", e)


def test_save_and_update_methods():
    """Test méthodes save() et update()"""
    try:
        amenity = Amenity("Pool")
        original_updated_at = amenity.updated_at
        
        import time
        time.sleep(0.01)
        amenity.save()
        assert amenity.updated_at > original_updated_at

        amenity.update({"name": "Swimming Pool"})
        assert amenity.name == "Swimming Pool"
        
        print("✅ Test réussi : méthodes save() et update()")
    except Exception as e:
        print("❌ Test échoué :", e)


if __name__ == "__main__":
    test_amenity_creation()
    test_invalid_name()
    test_empty_name()
    test_none_name()
    test_whitespace_name()
    test_valid_edge_cases()
    test_base_model_attributes()
    test_save_and_update_methods()
