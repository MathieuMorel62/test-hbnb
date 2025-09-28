#!/usr/bin/env python3
"""
Lanceur de tests global pour le projet HBNB
Ce fichier exécute tous les tests présents dans les différents modules
"""

import unittest
import sys
import os
import io
from pathlib import Path

# Ajout du chemin du projet à sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Import des tests des différents modules
from app.models.test.test_user import TestUser
from app.models.test.test_amenity import TestAmenity
from app.models.test.test_place import TestPlace
from app.models.test.test_review import TestReview
from app.api.v1.test.test_users_endpoints import TestUsersEndpoints
from app.services.test.test_facade import TestHBnBFacade

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


def discover_all_tests():
    """Découvre automatiquement tous les tests dans les modules"""
    test_modules = {
        'Models': [
            (TestUser, "Tests User (Models)"),
            (TestAmenity, "Tests Amenity (Models)"),
            (TestPlace, "Tests Place (Models)"),
            (TestReview, "Tests Review (Models)")
        ],
        'API': [
            (TestUsersEndpoints, "Tests Users Endpoints (API)"),
        ],
        'Services': [
            (TestHBnBFacade, "Tests HBnB Facade (Services)"),
        ],
        'Persistence': []
    }
    
    return test_modules


def run_all_tests():
    """Lance tous les tests unitaires du projet HBNB"""
    
    print("=" * 80)
    print("🧪 LANCEMENT DE TOUS LES TESTS DU PROJET HBNB")
    print("=" * 80)
    
    test_modules = discover_all_tests()
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    
    for module_name, test_classes in test_modules.items():
        if not test_classes:  # Skip empty modules
            continue
            
        print(f"\n📂 MODULE: {module_name}")
        print("=" * 60)
        
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
            print(f"   📊 Réussis: {successes}/{tests_run}")
            if failures > 0:
                print(f"   ❌ Échecs: {failures}")
            if errors > 0:
                print(f"   💥 Erreurs: {errors}")
    
    # Résumé global
    print("\n" + "=" * 80)
    print("📋 RÉSUMÉ GLOBAL")
    print("=" * 80)
    print(f"📈 Total des tests: {total_tests}")
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


def run_module_tests(module_name):
    """Lance les tests d'un module spécifique"""
    test_modules = discover_all_tests()
    
    if module_name.lower() not in [name.lower() for name in test_modules.keys()]:
        print(f"❌ Module '{module_name}' non trouvé")
        print(f"Modules disponibles: {', '.join(test_modules.keys())}")
        return False
    
    # Trouver le module correspondant
    target_module = None
    for name, tests in test_modules.items():
        if name.lower() == module_name.lower():
            target_module = (name, tests)
            break
    
    if not target_module or not target_module[1]:
        print(f"❌ Aucun test trouvé pour le module '{module_name}'")
        return False
    
    print(f"🧪 Lancement des tests pour le module: {target_module[0]}")
    print("=" * 60)
    
    total_success = True
    for test_class, description in target_module[1]:
        print(f"\n{description}")
        print("-" * 40)
        
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        if not result.wasSuccessful():
            total_success = False
    
    return total_success


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
    
    print(f"🧪 Lancement des tests pour: {test_class.__name__}")
    print("=" * 60)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def print_usage():
    """Affiche l'aide d'utilisation"""
    print("Usage:")
    print("  python test_all.py                    # Lance tous les tests")
    print("  python test_all.py --module models    # Lance les tests d'un module")
    print("  python test_all.py --class user       # Lance les tests d'une classe")
    print("  python test_all.py --help             # Affiche cette aide")
    print("\nModules disponibles: models, api, services, persistence")
    print("Classes disponibles: user, amenity, place, review")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Exécution de tous les tests
        success = run_all_tests()
        sys.exit(0 if success else 1)
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg in ['--help', '-h']:
            print_usage()
        else:
            success = run_specific_test(arg)
            sys.exit(0 if success else 1)
    elif len(sys.argv) == 3:
        flag = sys.argv[1]
        value = sys.argv[2]
        
        if flag == '--module':
            success = run_module_tests(value)
            sys.exit(0 if success else 1)
        elif flag == '--class':
            success = run_specific_test(value)
            sys.exit(0 if success else 1)
        else:
            print("❌ Option non reconnue")
            print_usage()
            sys.exit(1)
    else:
        print("❌ Trop d'arguments")
        print_usage()
        sys.exit(1)
