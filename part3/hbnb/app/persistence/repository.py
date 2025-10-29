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
