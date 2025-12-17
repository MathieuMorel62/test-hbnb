from abc import ABC, abstractmethod


class Repository(ABC):
    """
    Classe abstraite pour la gestion des opérations de persistance.
    """
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    """
    Implémentation de la classe Repository en mémoire.
    """
    def __init__(self):
        """
        Initialise le dépôt en mémoire.
        """
        self._storage = {}
        self._id_counter = 0

    def add(self, obj):
        """
        Ajoute un objet à la base de données.
        """
        self._storage[obj.id] = obj
        self._id_counter += 1

    def get(self, obj_id):
        """
        Récupère un objet par son identifiant.
        """
        return self._storage.get(obj_id)

    def get_all(self):
        """
        Récupère tous les objets de la base de données.
        """
        return list(self._storage.values())

    def update(self, obj_id, data):
        """
        Met à jour un objet existant dans la base de données.
        """
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """
        Supprime un objet de la base de données.
        """
        if obj_id in self._storage:
            del self._storage[obj_id]
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """
        Récupère un objet par une attribut spécifique.
        """
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)

class SQLAlchemyRepository(Repository):
    """
    Implémentation de la classe Repository avec SQLAlchemy.
    """
    def __init__(self, model):
        """
        Initialise le dépôt avec SQLAlchemy.
        """
        self.model = model

    def add(self, obj):
        """
        Ajoute un objet à la base de données.

        Args:
            obj: L'objet à ajouter à la base de données.
        """
        from app import db
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """
        Récupère un objet par son identifiant.

        Args:
            obj_id: Identifiant de l'objet à récupérer.

        Returns:
            Objet trouvé ou None si inexistant.
        """
        return self.model.query.get(obj_id)
    
    def get_all(self):
        """
        Récupère tous les objets de la base de données.

        Returns:
            list: Liste de tous les objets.
        """
        return self.model.query.all()

    def update(self, obj_id, data):
        """
        Met à jour un objet existant dans la base de données.

        Args:
            obj_id: Identifiant de l'objet à mettre à jour.
            data (dict): Dictionnaire contenant les données à mettre à jour.
        """
        from app import db
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        """
        Supprime un objet de la base de données.

        Args:
            obj_id: Identifiant de l'objet à supprimer.
        
        Returns:
            bool: True si l'objet a été supprimé, False sinon.
        """
        from app import db
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """
        Récupère un objet par une attribut spécifique.

        Args:
            attr_name (str): Nom de l'attribut à rechercher.
            attr_value (any): Valeur de l'attribut à rechercher.

        Returns:
            Objet trouvé ou None si inexistant.
        """
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
