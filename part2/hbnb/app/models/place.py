from .base_model import BaseModel
from .user import User


class Place(BaseModel):
    """Classe pour la gestion des lieux"""
    def __init__(self, title, description, price, latitude, longitude, owner):
        """Initialisation des attributs de l'objet"""
        super().__init__()

        # Validation des attributs
        if not title or len(title) > 100:
            raise ValueError("The title is required and must be a maximum of 100 characters.")
        if price <= 0:
            raise ValueError("The price must be a positive number.")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("The latitude must be between -90.0 and 90.0")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("The longitude must be between -180.0 and 180.0.")
        if not isinstance(owner, User):
            raise TypeError("The owner must be an instance of the User class.")
        
        # Initialisation des attributs de l'objet
        self.title = title
        self.description = description or ""
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

        # Initialisation des listes vides
        self.reviews = []
        self.amenities = []
    

    def add_review(self, review):
        """Ajoute une review à la liste des reviews"""
        self.reviews.append(review)
    

    def add_amenity(self, amenity):
        """Ajoute une amenity à la liste des amenities"""
        self.amenities.append(amenity)
