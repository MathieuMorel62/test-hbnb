from .base_model import BaseModel
import re


class User(BaseModel):
    """Classe pour la gestion des utilisateurs"""
    def __init__(self, first_name, last_name, email, is_admin=False):
        """Initialisation des attributs de l'objet"""
        super().__init__()
        if not first_name or len(first_name) > 50:
            raise ValueError("first_name is required and must be at most 50 characters")
        if not last_name or len(last_name) > 50:
            raise ValueError("last_name is required and must be at most 50 characters")
        if not self.validate_email(email):
            raise ValueError("email must be a valid email address")

        # Initialisation des attributs de l'objet
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin


    def validate_email(self, email):
        """Validation de l'email"""
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(regex, email) is not None
