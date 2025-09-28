# 🧪 Organisation des Tests HBNB

## 📁 Structure des Tests

La nouvelle organisation des tests suit une structure modulaire pour un meilleur suivi et organisation :

```
hbnb/
├── test_all.py                    # Lanceur global de tous les tests
├── app/
│   ├── models/
│   │   └── test/
│   │       ├── __init__.py
│   │       ├── run_tests.py       # Tests du module Models
│   │       ├── test_user.py
│   │       ├── test_amenity.py
│   │       ├── test_place.py
│   │       └── test_review.py
│   ├── api/
│   │   └── test/
│   │       ├── __init__.py
│   │       └── run_tests.py       # Tests du module API (à développer)
│   ├── services/
│   │   └── test/
│   │       ├── __init__.py
│   │       └── run_tests.py       # Tests du module Services (à développer)
│   └── persistence/
│       └── test/
│           ├── __init__.py
│           └── run_tests.py       # Tests du module Persistence (à développer)
```

## 🚀 Comment Exécuter les Tests

### 1. Tous les Tests
```bash
cd hbnb
python3 test_all.py
```

### 2. Tests par Module
```bash
# Tests des modèles
python3 test_all.py --module models

# Tests de l'API (quand ils seront créés)
python3 test_all.py --module api

# Tests des services (quand ils seront créés)
python3 test_all.py --module services

# Tests de la persistance (quand ils seront créés)
python3 test_all.py --module persistence
```

### 3. Tests d'une Classe Spécifique
```bash
# Tests de User
python3 test_all.py --class user

# Tests d'Amenity
python3 test_all.py --class amenity

# Tests de Place
python3 test_all.py --class place

# Tests de Review
python3 test_all.py --class review
```

### 4. Tests d'un Module Spécifique (depuis le dossier du module)
```bash
# Tests des modèles depuis leur dossier
cd app/models/test
python3 run_tests.py

# Tests de l'API depuis leur dossier
cd app/api/test
python3 run_tests.py
```

### 5. Aide
```bash
python3 test_all.py --help
```

## 📊 Format des Résultats

Le lanceur global affiche :
- 🧪 Module en cours de test
- ✅ Tests réussis
- ❌ Tests échoués
- 💥 Erreurs
- 📊 Statistiques par classe
- 📋 Résumé global final

## 🔧 Ajouter de Nouveaux Tests

### Pour les Modèles
1. Créez votre fichier de test dans `app/models/test/`
2. Importez-le dans `app/models/test/run_tests.py`
3. Ajoutez la classe dans `test_all.py`

### Pour l'API
1. Créez vos fichiers de test dans `app/api/test/`
2. Mettez à jour `app/api/test/run_tests.py`
3. Ajoutez les classes dans `test_all.py`

### Pour les Services
1. Créez vos fichiers de test dans `app/services/test/`
2. Mettez à jour `app/services/test/run_tests.py`
3. Ajoutez les classes dans `test_all.py`

### Pour la Persistance
1. Créez vos fichiers de test dans `app/persistence/test/`
2. Mettez à jour `app/persistence/test/run_tests.py`
3. Ajoutez les classes dans `test_all.py`

## 🎯 Avantages de Cette Organisation

- ✅ **Modularité** : Tests organisés par module fonctionnel
- ✅ **Scalabilité** : Facile d'ajouter de nouveaux modules de tests
- ✅ **Flexibilité** : Possibilité d'exécuter des tests spécifiques
- ✅ **Maintenance** : Structure claire et logique
- ✅ **CI/CD** : Compatible avec les pipelines d'intégration continue

## 📈 Statistiques Actuelles

- **Total des tests** : 39
- **Modules testés** : Models (User, Amenity, Place, Review)
- **Modules à développer** : API, Services, Persistence
- **Taux de réussite** : 100%
