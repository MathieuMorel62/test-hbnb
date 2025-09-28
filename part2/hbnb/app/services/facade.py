from app.persistence.repository import InMemoryRepository
from app.models.user import User


class HBnBFacade:
    """
    Facade pour la gestion des opérations de l'application.
    """
    def __init__(self):
        """
        Initialise les dépôts en mémoire.
        """
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()


    def create_user(self, user_data):
        """
        Crée un utilisateur.

        Args:
            user_data (dict): Données de l'utilisateur à créer.
        
        Returns:
            User: L'utilisateur créé.
        """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """
        Récupère un utilisateur par son identifiant.

        Args:
            user_id (str): Identifiant de l'utilisateur.
        
        Returns:
            User: L'utilisateur trouvé.
        """
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """
        Récupère tous les utilisateurs.
        
        Returns:
            list: Liste des utilisateurs.
        """
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        """
        Récupère un utilisateur par son email.

        Args:
            email (str): Email de l'utilisateur.
        
        Returns:
            User: L'utilisateur trouvé.
        """
        return self.user_repo.get_by_attribute('email', email)
    
    def update_user(self, user_id, user_data):
        """
        Met à jour un utilisateur.

        Args:
            user_id (str): Identifiant de l'utilisateur.
            user_data (dict): Données de l'utilisateur à mettre à jour.
        
        Returns:
            User: L'utilisateur mis à jour.
        """
        user = self.get_user(user_id)
        if user:
            # Vérification de l'email unique lors de la mise à jour
            if 'email' in user_data and user_data['email'] != user.email:
                existing_user = self.get_user_by_email(user_data['email'])
                if existing_user:
                    raise ValueError("Email already registered")
            # Mise à jour des données de l'utilisateur
            self.user_repo.update(user_id, user_data)
            return user
        return None

    def get_place(self, place_id):
        """
        Récupère un lieu par son identifiant.

        Args:
            place_id (str): Identifiant du lieu.
        
        Returns:
            Place: Le lieu trouvé.
        """
        return self.place_repo.get(place_id)

    def create_place(self, place_data):
        pass

    def create_review(self, review_data):
        pass

    def create_amenity(self, amenity_data):
        pass
