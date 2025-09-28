#!/usr/bin/env python3
"""
Lanceur de tests pour le module API
"""

import unittest
import sys
import os

# Ajout du chemin du projet à sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

def run_api_tests():
    """Lance tous les tests du module API"""
    
    print("=" * 60)
    print("🧪 TESTS DU MODULE API")
    print("=" * 60)
    
    # TODO: Ajouter les classes de tests API quand elles seront créées
    # test_classes = []
    
    print("ℹ️  Aucun test API n'est encore défini.")
    
    return True


if __name__ == "__main__":
    success = run_api_tests()
    sys.exit(0 if success else 1)
