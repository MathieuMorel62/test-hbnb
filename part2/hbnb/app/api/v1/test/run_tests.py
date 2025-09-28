#!/usr/bin/env python3
"""
Lanceur de tests pour l'API v1
"""

import unittest
import sys
import os

# Ajout du chemin du projet à sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from test_users_endpoints import TestUsersEndpoints


def run_api_v1_tests():
    """Lance tous les tests de l'API v1"""
    
    print("=" * 60)
    print("🧪 TESTS DE L'API V1")
    print("=" * 60)
    
    # Classes de tests disponibles
    test_classes = [
        TestUsersEndpoints
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


def run_specific_test(test_name):
    """Lance un test spécifique"""
    test_classes = {
        'users': TestUsersEndpoints,
        'users_endpoints': TestUsersEndpoints
    }
    
    if test_name.lower() not in test_classes:
        print(f"❌ Test '{test_name}' non trouvé")
        print(f"Tests disponibles: {', '.join(test_classes.keys())}")
        return False
    
    test_class = test_classes[test_name.lower()]
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    
    print(f"🧪 Lancement des tests pour: {test_class.__name__}")
    print("=" * 60)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Exécution d'un test spécifique
        test_name = sys.argv[1]
        success = run_specific_test(test_name)
    else:
        # Exécution de tous les tests
        success = run_api_v1_tests()
    
    sys.exit(0 if success else 1)
