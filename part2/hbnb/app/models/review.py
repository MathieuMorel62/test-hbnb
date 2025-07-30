from .base_model import BaseModel
from .user import User
from .place import Place


class Review(BaseModel):
    """Classe pour la gestion des reviews"""
    def __init__(self, text, rating, place, user):
        super().__init__()

        # Validation des attributs
        if not text or not isinstance(text, str):
            raise ValueError("The text of the notice is required.")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("The note must be an integer between 1 and 5.")
        if not isinstance(place, Place):
            raise TypeError("The place must be an instance of the Place class.")
        if not isinstance(user, User):
            raise TypeError("The user must be an instance of the User class.")
        

        # Initialisation des attributs de l'objet
        self.text = text
        self.rating = rating
        self.user = user
        self.place = place
