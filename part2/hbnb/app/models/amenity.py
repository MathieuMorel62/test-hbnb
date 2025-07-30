from .base_model import BaseModel


class Amenity(BaseModel):
    """Classe pour la gestion des équipements"""
    def __init__(self, name):
        super().__init__()

        # Validation des attributs
        if not name or len(name) > 50:
            raise ValueError("The name of the equipment is required and must be less than 50 characters.")
        
        # Initialisation des attributs de l'objet
        self.name = name
