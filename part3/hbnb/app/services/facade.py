from app.persistence.repository import InMemoryRepository, SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    """
    Facade pour la gestion des opérations de l'application.
    """
    def __init__(self, repositories=None):
        """
        Initialise les dépôts en mémoire.
        
        Args:
            repositories (dict): Dépôts à utiliser (pour les tests)
            Si None, utilise SQLAlchemyRepository par défaut.
        """
        if repositories:
            self.user_repo = repositories.get('user_repo', SQLAlchemyRepository(User))
            self.place_repo = repositories.get('place_repo', SQLAlchemyRepository(Place))
            self.review_repo = repositories.get('review_repo', SQLAlchemyRepository(Review))
            self.amenity_repo = repositories.get('amenity_repo', SQLAlchemyRepository(Amenity))
        else:
            self.user_repo = SQLAlchemyRepository(User)
            self.place_repo = SQLAlchemyRepository(Place)
            self.review_repo = SQLAlchemyRepository(Review)
            self.amenity_repo = SQLAlchemyRepository(Amenity)


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
        if not user_id:
            return None
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
        # Création de l'équipement
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
        if not amenity_id:
            return None
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
            # Mise à jour de l'équipement
            self.amenity_repo.update(amenity_id, amenity_data)
            return amenity
        return None

    def create_place(self, place_data):
        """
        Crée un nouveau lieu.

        Args:
            place_data (dict): Données du lieu à créer.
        
        Returns:
            Place: Le lieu créé.
        
        Raises:
            ValueError: Si les données sont invalides.
            TypeError: Si le propriétaire n'est pas valide.
        """
        # Validation du propriétaire 
        owner = self.get_user(place_data.get('owner_id'))
        if not owner:
            raise ValueError("Owner not found")

        # Validation des données numériques
        try:
            price = float(place_data['price'])
            if price <= 0:
                raise ValueError("Price must be positive")
            latitude = float(place_data['latitude'])
            if not (-90.0 <= latitude <= 90.0):
                raise ValueError("Latitude must be between -90 and 90")
            longitude = float(place_data['longitude'])
            if not (-180.0 <= longitude <= 180.0):
                raise ValueError("Longitude must be between -180 and 180")
        except (ValueError, TypeError, KeyError):
            raise ValueError("Invalid numeric values")

        # Récupération des amenities si fournis 
        amenities = []
        if 'amenities' in place_data:
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with id {amenity_id} not found")
                amenities.append(amenity)

        # Création du lieu avec les données fournies
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner=owner
        )

        # Ajout des amenities au lieu
        for amenity in amenities:
            place.add_amenity(amenity)

        # Sauvegarde du lieu dans le repository
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """
        Récupère un lieu par son identifiant.

        Args:
            place_id (str): Identifiant du lieu.
        
        Returns:
            Place: Le lieu trouvé.
        """
        if not place_id:
            return None
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """
        Récupère tous les lieux.
        
        Returns:
            list: Liste des lieux.
        """
        return self.place_repo.get_all()
    
    def update_place(self, place_id, place_data):
        """
        Met à jour un lieu.

        Args:
            place_id (str): Identifiant du lieu.
            place_data (dict): Données du lieu à mettre à jour.
        
        Returns:
            Place: Le lieu mis à jour.
        """
        place = self.get_place(place_id)
        if not place:
            return None
        
        # Validation des données numériques avant la mise à jour
        if 'price' in place_data:
            if float(place_data['price']) <= 0:
                raise ValueError("The price must be a positive number.")
        if 'latitude' in place_data:
            if not (-90.0 <= float(place_data['latitude']) <= 90.0):
                raise ValueError("The latitude must be between -90.0 and 90.0")
        if 'longitude' in place_data:
            if not (-180.0 <= float(place_data['longitude']) <= 180.0):
                raise ValueError("The longitude must be between -180.0 and 180.0")
        
        # Mise à jour des amenities si fournis
        if 'amenities' in place_data:
            new_amenities = []
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with id {amenity_id} not found")
                new_amenities.append(amenity_id)
            place.amenities = new_amenities
        
        # Suppression des amenities de la donnée à mettre à jour
        update_data = place_data.copy()
        if 'amenities' in update_data:
            del update_data['amenities']
        
        # Mise à jour du lieu dans le repo
        self.place_repo.update(place_id, update_data)
        return place

    def create_review(self, review_data):
        """
        Crée une nouvelle review.

        Args:
            review_data (dict): Données de la review à créer.
        
        Returns:
            Review: La review créée.
        
        Raises:
            ValueError: Si les données sont invalides.
        """
        # Validation des données avant la création
        place = self.get_place(review_data.get('place_id'))
        if not place:
            raise ValueError("Place not found")

        # Validation de l'utilisateur
        user = self.get_user(review_data.get('user_id'))
        if not user:
            raise ValueError("User not found")

        # Validation du rating
        try:
            rating = int(review_data['rating'])
            if not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5")
        except (ValueError, TypeError):
            raise ValueError("Rating must be an integer between 1 and 5")
        
        # Création de la review
        review = Review(
            text=review_data['text'],
            rating=rating,
            place=place,
            user=user
        )
        # Sauvegarde de la review dans le repository
        self.review_repo.add(review)
        return review

    
    def get_review(self, review_id):
        """
        Récupère une review par son identifiant.

        Args:
            review_id (str): Identifiant de la review.
        
        Returns:
            Review: La review trouvée.
        """
        if not review_id:
            return None
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Récupère toutes les reviews.
        
        Returns:
            list: Liste des reviews.
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Récupère toutes les reviews d'un lieu.

        Args:
            place_id (str): Identifiant du lieu.
        
        Returns:
            list: Liste des reviews.
        """
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        return [review for review in self.review_repo.get_all()
                if review.place.id == place_id]
    
    def update_review(self, review_id, review_data):
        """
        Met à jour une review.

        Args:
            review_id (str): Identifiant de la review.
            review_data (dict): Données de la review à mettre à jour.
        
        Returns:
            Review: La review mise à jour.
        """
        # Validation de la review
        review = self.get_review(review_id)
        if not review:
            return None
        
        # Validation de la note
        if 'rating' in review_data:
            rating = int(review_data['rating'])
            if not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5")
        
        # Mise à jour de la review dans le repository
        self.review_repo.update(review_id, review_data)
        return review
    
    def delete_review(self, review_id):
        """
        Supprime une review.

        Args:
            review_id (str): Identifiant de la review.
        
        Returns:
            bool: True si la review a été supprimée, False sinon.
        """
        # Validation de la review
        review = self.get_review(review_id)
        if not review:
            return False
        
        # Suppression de la review dans le repository
        return self.review_repo.delete(review_id)
