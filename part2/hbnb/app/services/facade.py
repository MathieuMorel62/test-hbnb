from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity


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
    
    def create_amenity(self, amenity_data):
        """
        Crée un équipement.

        Args:
            amenity_data (dict): Données de l'équipement à créer.
        
        Returns:
            Amenity: L'équipement créé.
        """
        # Validation des données avant création
        if 'name' in amenity_data:
            name = amenity_data['name']
            if not name or len(name.strip()) == 0 or len(name) > 50:
                raise ValueError("The name of the equipment is required and must be less than 50 characters.")
        
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """
        Récupère un équipement par son identifiant.

        Args:
            amenity_id (str): Identifiant de l'équipement.
        
        Returns:
            Amenity: L'équipement trouvé.
        """
        return self.amenity_repo.get(amenity_id)
    
    def get_all_amenities(self):
        """
        Récupère tous les équipements.
        
        Returns:
            list: Liste des équipements.
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Met à jour un équipement.

        Args:
            amenity_id (str): Identifiant de l'équipement.
            amenity_data (dict): Données de l'équipement à mettre à jour.

        Returns:
            Amenity: L'équipement mis à jour.
        """
        amenity = self.get_amenity(amenity_id)
        if amenity:
            # Validation des données avant la mise à jour
            if 'name' in amenity_data:
                name = amenity_data['name']
                if not name or len(name.strip()) == 0 or len(name) > 50:
                    raise ValueError("The name of the equipment is required and must be less than 50 characters.")

            self.amenity_repo.update(amenity_id, amenity_data)
            return amenity
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
