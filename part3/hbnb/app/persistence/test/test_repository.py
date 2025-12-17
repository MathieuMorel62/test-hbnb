import sys
import os
import unittest
from abc import ABC

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from app.persistence.repository import Repository, InMemoryRepository, SQLAlchemyRepository


class TestRepositoryInterface(unittest.TestCase):
    """Tests pour vérifier que les repositories implémentent correctement l'interface Repository"""

    def test_inmemory_repository_is_repository_instance(self):
        """Test que InMemoryRepository est une instance de Repository"""
        repo = InMemoryRepository()
        self.assertIsInstance(repo, Repository)
        # Repository hérite de ABC, donc c'est normal que ce soit aussi une instance d'ABC
        self.assertIsInstance(repo, ABC)

    def test_sqlalchemy_repository_is_repository_instance(self):
        """Test que SQLAlchemyRepository est une instance de Repository"""
        # Utiliser un modèle factice pour tester la structure
        class FakeModel:
            query = None
        
        repo = SQLAlchemyRepository(FakeModel)
        self.assertIsInstance(repo, Repository)
        # Repository hérite de ABC, donc c'est normal que ce soit aussi une instance d'ABC
        self.assertIsInstance(repo, ABC)

    def test_inmemory_repository_has_all_methods(self):
        """Test que InMemoryRepository a toutes les méthodes requises"""
        repo = InMemoryRepository()
        self.assertTrue(hasattr(repo, 'add'))
        self.assertTrue(hasattr(repo, 'get'))
        self.assertTrue(hasattr(repo, 'get_all'))
        self.assertTrue(hasattr(repo, 'update'))
        self.assertTrue(hasattr(repo, 'delete'))
        self.assertTrue(hasattr(repo, 'get_by_attribute'))

    def test_sqlalchemy_repository_has_all_methods(self):
        """Test que SQLAlchemyRepository a toutes les méthodes requises"""
        class FakeModel:
            query = None
        
        repo = SQLAlchemyRepository(FakeModel)
        self.assertTrue(hasattr(repo, 'add'))
        self.assertTrue(hasattr(repo, 'get'))
        self.assertTrue(hasattr(repo, 'get_all'))
        self.assertTrue(hasattr(repo, 'update'))
        self.assertTrue(hasattr(repo, 'delete'))
        self.assertTrue(hasattr(repo, 'get_by_attribute'))

    def test_sqlalchemy_repository_stores_model(self):
        """Test que SQLAlchemyRepository stocke correctement le modèle"""
        class FakeModel:
            query = None
        
        repo = SQLAlchemyRepository(FakeModel)
        self.assertEqual(repo.model, FakeModel)


class TestInMemoryRepository(unittest.TestCase):
    """Tests pour InMemoryRepository"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.repo = InMemoryRepository()

    def test_add_object(self):
        """Test l'ajout d'un objet"""
        class TestObj:
            def __init__(self, obj_id):
                self.id = obj_id
        
        obj = TestObj("test-id")
        self.repo.add(obj)
        self.assertIn("test-id", self.repo._storage)
        self.assertEqual(self.repo._storage["test-id"], obj)

    def test_get_object(self):
        """Test la récupération d'un objet"""
        class TestObj:
            def __init__(self, obj_id):
                self.id = obj_id
        
        obj = TestObj("test-id")
        self.repo.add(obj)
        retrieved = self.repo.get("test-id")
        self.assertEqual(retrieved, obj)

    def test_get_nonexistent_object(self):
        """Test la récupération d'un objet inexistant"""
        result = self.repo.get("nonexistent")
        self.assertIsNone(result)

    def test_get_all_objects(self):
        """Test la récupération de tous les objets"""
        class TestObj:
            def __init__(self, obj_id):
                self.id = obj_id
        
        obj1 = TestObj("id1")
        obj2 = TestObj("id2")
        self.repo.add(obj1)
        self.repo.add(obj2)
        
        all_objects = self.repo.get_all()
        self.assertEqual(len(all_objects), 2)
        self.assertIn(obj1, all_objects)
        self.assertIn(obj2, all_objects)

    def test_update_object(self):
        """Test la mise à jour d'un objet"""
        class TestObj:
            def __init__(self, obj_id, name):
                self.id = obj_id
                self.name = name
            
            def update(self, data):
                for key, value in data.items():
                    setattr(self, key, value)
        
        obj = TestObj("test-id", "old-name")
        self.repo.add(obj)
        self.repo.update("test-id", {"name": "new-name"})
        self.assertEqual(obj.name, "new-name")

    def test_delete_object(self):
        """Test la suppression d'un objet"""
        class TestObj:
            def __init__(self, obj_id):
                self.id = obj_id
        
        obj = TestObj("test-id")
        self.repo.add(obj)
        result = self.repo.delete("test-id")
        self.assertTrue(result)
        self.assertNotIn("test-id", self.repo._storage)

    def test_delete_nonexistent_object(self):
        """Test la suppression d'un objet inexistant"""
        result = self.repo.delete("nonexistent")
        self.assertFalse(result)

    def test_get_by_attribute(self):
        """Test la récupération par attribut"""
        class TestObj:
            def __init__(self, obj_id, email):
                self.id = obj_id
                self.email = email
        
        obj1 = TestObj("id1", "email1@test.com")
        obj2 = TestObj("id2", "email2@test.com")
        self.repo.add(obj1)
        self.repo.add(obj2)
        
        result = self.repo.get_by_attribute("email", "email1@test.com")
        self.assertEqual(result, obj1)
        
        result = self.repo.get_by_attribute("email", "nonexistent@test.com")
        self.assertIsNone(result)


class TestSQLAlchemyRepositoryStructure(unittest.TestCase):
    """Tests pour vérifier la structure de SQLAlchemyRepository"""
    # Note: Ces tests vérifient uniquement la structure, pas le fonctionnement
    # car les modèles ne sont pas encore mappés à SQLAlchemy

    def test_sqlalchemy_repository_initialization(self):
        """Test l'initialisation de SQLAlchemyRepository"""
        class FakeModel:
            query = None
        
        repo = SQLAlchemyRepository(FakeModel)
        self.assertEqual(repo.model, FakeModel)

    def test_sqlalchemy_repository_methods_are_callable(self):
        """Test que les méthodes de SQLAlchemyRepository sont callable"""
        class FakeModel:
            class Query:
                @staticmethod
                def get(obj_id):
                    return None
                
                @staticmethod
                def all():
                    return []
                
                @staticmethod
                def filter_by(**kwargs):
                    class FilterResult:
                        @staticmethod
                        def first():
                            return None
                    return FilterResult()
            
            query = Query()
        
        repo = SQLAlchemyRepository(FakeModel)
        # Vérifier que les méthodes existent et sont callable
        self.assertTrue(callable(repo.add))
        self.assertTrue(callable(repo.get))
        self.assertTrue(callable(repo.get_all))
        self.assertTrue(callable(repo.update))
        self.assertTrue(callable(repo.delete))
        self.assertTrue(callable(repo.get_by_attribute))


if __name__ == '__main__':
    unittest.main()

