#!/usr/bin/env python3

import subprocess
import os


def run_test(test_file):
    """Exécute un fichier de test et affiche le résultat"""
    print(f"\n{'='*50}")
    print(f"EXÉCUTION DE {test_file}")
    print('='*50)
    
    try:
        result = subprocess.run(['python3', test_file], 
                              capture_output=True, 
                              text=True, 
                              cwd=os.path.dirname(os.path.abspath(__file__)))
        
        print(result.stdout)
        if result.stderr:
            print("❌ ERREURS:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")

def main():
    """Exécute tous les tests"""
    print("LANCEMENT DE TOUS LES TESTS DU PROJET HBNB")
    
    tests = [
        'test_user.py',
        'test_amenity.py', 
        'test_review.py',
        'test_place.py'
    ]
    
    for test in tests:
        run_test(test)
    
    print(f"\n{'='*50}")
    print("✅ TOUS LES TESTS TERMINÉS")
    print('='*50)


if __name__ == "__main__":
    main()
