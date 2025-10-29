from .base_model import BaseModel
import re


class User(BaseModel):
    """Classe pour la gestion des utilisateurs"""
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """Initialisation des attributs de l'objet"""
        super().__init__()
        if not first_name or len(first_name) > 50:
            raise ValueError("first_name is required and must be at most 50 characters")
        if not last_name or len(last_name) > 50:
            raise ValueError("last_name is required and must be at most 50 characters")
        if not self.validate_email(email):
            raise ValueError("email must be a valid email address")
        if not password:
            raise ValueError("password is required")
        self.hash_password(password)

        # Initialisation des attributs de l'objet
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin


    def validate_email(self, email):
        """Validation de l'email"""
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(regex, email) is not None

    def hash_password(self, password):
        """Hashes the password before storing it."""
        from app import bcrypt
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        from app import bcrypt
        return bcrypt.check_password_hash(self.password, password)
