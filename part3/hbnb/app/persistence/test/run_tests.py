#!/usr/bin/env python3
"""
Lanceur de tests pour le module Persistence
"""

import unittest
import sys
import os

# Ajout du chemin du projet à sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

def run_persistence_tests():
    """Lance tous les tests du module Persistence"""
    
    print("=" * 60)
    print("🧪 TESTS DU MODULE PERSISTENCE")
    print("=" * 60)
    
    # TODO: Ajouter les classes de tests Persistence quand elles seront créées
    # test_classes = []
    
    print("ℹ️  Aucun test Persistence n'est encore défini.")    
    return True


if __name__ == "__main__":
    success = run_persistence_tests()
    sys.exit(0 if success else 1)
