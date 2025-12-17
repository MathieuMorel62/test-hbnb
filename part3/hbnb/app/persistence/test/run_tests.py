#!/usr/bin/env python3
"""
Lanceur de tests pour le module Persistence
"""

import unittest
import sys
import os

# Ajout du chemin du projet à sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from app.persistence.test.test_repository import (
    TestRepositoryInterface,
    TestInMemoryRepository,
    TestSQLAlchemyRepositoryStructure
)


def run_persistence_tests():
    """Lance tous les tests du module Persistence"""
    
    print("=" * 60)
    print("🧪 TESTS DU MODULE PERSISTENCE")
    print("=" * 60)
    
    test_classes = [
        (TestRepositoryInterface, "Tests Interface Repository"),
        (TestInMemoryRepository, "Tests InMemoryRepository"),
        (TestSQLAlchemyRepositoryStructure, "Tests Structure SQLAlchemyRepository")
    ]
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    for test_class, description in test_classes:
        print(f"\n{description}")
        print("-" * 40)
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_persistence_tests()
    sys.exit(0 if success else 1)
