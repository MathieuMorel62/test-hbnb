#!/usr/bin/env python3

import unittest
import sys
import os
import io

# Ajout du chemin du projet à sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import des tests
from test_user import TestUser
from test_amenity import TestAmenity
from test_place import TestPlace
from test_review import TestReview


class ColoredTestResult(unittest.TextTestResult):
    """Résultat de test avec couleurs et format amélioré"""
    
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.success_count = 0
        self.verbosity = verbosity
        
    def addSuccess(self, test):
        super().addSuccess(test)
        self.success_count += 1
        print(f"✅ {test._testMethodDoc or test._testMethodName}")
            
    def addFailure(self, test, err):
        super().addFailure(test, err)
        print(f"❌ {test._testMethodDoc or test._testMethodName}")
        
    def addError(self, test, err):
        super().addError(test, err)
        print(f"💥 {test._testMethodDoc or test._testMethodName}")


def run_all_tests():
    """Lance tous les tests unitaires du projet HBNB"""
    
    print("=" * 60)
    print("LANCEMENT DE TOUS LES TESTS DU PROJET HBNB")
    print("=" * 60)
    
    # Classes de tests avec leurs noms affichés
    test_classes = [
        (TestUser, "Tests User"),
        (TestAmenity, "Tests Amenity"), 
        (TestPlace, "Tests Place"),
        (TestReview, "Tests Review")
    ]
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    
    for test_class, description in test_classes:
        print(f"\n{description}")
        print("-" * 40)
        
        # Créer une suite pour cette classe
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        
        # Capturer la sortie pour un format personnalisé
        stream = io.StringIO()
        runner = unittest.TextTestRunner(
            stream=stream,
            verbosity=0,
            resultclass=ColoredTestResult
        )
        
        result = runner.run(suite)
        
        # Compter les résultats
        tests_run = result.testsRun
        failures = len(result.failures)
        errors = len(result.errors)
        successes = tests_run - failures - errors
        
        total_tests += tests_run
        total_failures += failures
        total_errors += errors
        
        # Afficher le résumé pour cette classe
        print(f"   Réussis: {successes}/{tests_run}")
        if failures > 0:
            print(f"   Échecs: {failures}")
        if errors > 0:
            print(f"   Erreurs: {errors}")
    
    # Résumé global
    print("\n" + "=" * 60)
    print("RÉSUMÉ GLOBAL")
    print("=" * 60)
    print(f"Total des tests: {total_tests}")
    print(f"✅ Réussis: {total_tests - total_failures - total_errors}")
    
    if total_failures > 0:
        print(f"❌ Échecs: {total_failures}")
    if total_errors > 0:
        print(f"💥 Erreurs: {total_errors}")
    
    if total_failures == 0 and total_errors == 0:
        print("\n🎉 TOUS LES TESTS ONT RÉUSSI!")
        return True
    else:
        print(f"\n⚠️  {total_failures + total_errors} test(s) ont échoué")
        return False


def run_specific_test(test_class_name):
    """Lance les tests d'une classe spécifique"""
    test_classes = {
        'user': TestUser,
        'amenity': TestAmenity,
        'place': TestPlace,
        'review': TestReview
    }
    
    if test_class_name.lower() not in test_classes:
        print(f"❌ Classe de test '{test_class_name}' non trouvée")
        print(f"Classes disponibles: {', '.join(test_classes.keys())}")
        return False
    
    test_class = test_classes[test_class_name.lower()]
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    
    print(f"Lancement des tests pour: {test_class.__name__}")
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Exécution d'une classe de tests spécifique
        test_name = sys.argv[1]
        run_specific_test(test_name)
    else:
        # Exécution de tous les tests
        run_all_tests()