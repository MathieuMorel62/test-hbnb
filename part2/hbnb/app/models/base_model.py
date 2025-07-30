import uuid
from datetime import datetime


class BaseModel:
    """Classe de base pour tous les modèles"""
    def __init__(self):
        """Initialisation des attributs de l'objet"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Met à jour l'attribut updated_at"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Met à jour les attributs passés dans le dictionnaire data"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
