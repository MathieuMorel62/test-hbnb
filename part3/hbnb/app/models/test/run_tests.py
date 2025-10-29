#!/usr/bin/env python3
"""
Lanceur de tests pour le module Models
"""

import unittest
import sys
import os

# Ajout du chemin du projet à sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from test_user import TestUser
from test_amenity import TestAmenity
from test_place import TestPlace
from test_review import TestReview


def run_models_tests():
    """Lance tous les tests du module Models"""
    
    print("=" * 60)
    print("🧪 TESTS DU MODULE MODELS")
    print("=" * 60)
    
    # Classes de tests
    test_classes = [
        TestUser,
        TestAmenity,
        TestPlace,
        TestReview
    ]
    
    # Créer une suite avec tous les tests
    suite = unittest.TestSuite()
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Résumé
    print(f"\n📊 Résultats:")
    print(f"✅ Tests réussis: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Échecs: {len(result.failures)}")
    print(f"💥 Erreurs: {len(result.errors)}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_models_tests()
    sys.exit(0 if success else 1)
