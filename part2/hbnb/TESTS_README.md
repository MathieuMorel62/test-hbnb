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
│   │   └── v1/
│   │       └── test/
│   │           ├── __init__.py
│   │           ├── run_tests.py   # Tests de l'API v1
│   │           ├── test_users_endpoints.py
│   │           └── test_amenities_endpoints.py
│   ├── services/
│   │   └── test/
│   │       ├── __init__.py
│   │       ├── run_tests.py       # Tests du module Services
│   │       ├── test_facade.py
│   │       └── test_amenities_facade.py
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

# Tests de l'API
python3 test_all.py --module api

# Tests des services
python3 test_all.py --module services

# Tests de la persistance (à développer)
python3 test_all.py --module persistence
```

### 3. Tests d'une Classe Spécifique
```bash
# Tests de User (modèle)
python3 test_all.py --class user

# Tests d'Amenity (modèle)
python3 test_all.py --class amenity

# Tests de Place (modèle)
python3 test_all.py --class place

# Tests de Review (modèle)
python3 test_all.py --class review

# Tests des endpoints utilisateurs (API)
python3 test_all.py --class users_endpoints

# Tests des endpoints amenities (API)
python3 test_all.py --class amenities_endpoints

# Tests de la facade (Services)
python3 test_all.py --class facade

# Tests de la facade amenities (Services)
python3 test_all.py --class amenities_facade
```

### 4. Tests d'un Module Spécifique (depuis le dossier du module)
```bash
# Tests des modèles depuis leur dossier
cd app/models/test
python3 run_tests.py

# Tests de l'API v1 depuis leur dossier
cd app/api/v1/test
python3 run_tests.py

# Tests des services depuis leur dossier
cd app/services/test
python3 run_tests.py

# Tests spécifiques dans un module
cd app/api/v1/test
python3 run_tests.py users_endpoints
python3 run_tests.py amenities_endpoints

cd app/services/test
python3 run_tests.py facade
python3 run_tests.py amenities_facade
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
1. Créez vos fichiers de test dans `app/api/v1/test/`
2. Mettez à jour `app/api/v1/test/run_tests.py`
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

- **Total des tests** : 85+ (39 Models + 23 API + 23+ Services)
- **Modules testés** : 
  - ✅ **Models** : User, Amenity, Place, Review (39 tests)
  - ✅ **API v1** : Users Endpoints (13 tests) + Amenities Endpoints (10 tests)
  - ✅ **Services** : HBnB Facade (13+ tests) + Amenities Facade (10+ tests)
- **Modules à développer** : Persistence
- **Taux de réussite** : 100% ✅
- **Couverture** : 100% des fonctionnalités développées

## 🎯 Types de Tests Couverts

### **Tests de Modèles (Models)**
- Validation des données
- Contraintes de longueur
- Formats d'email
- Relations entre objets
- Méthodes de mise à jour

### **Tests d'API (Endpoints)**
- ✅ Création d'utilisateurs (POST)
  - Succès avec données valides
  - Échec avec email déjà existant
  - Échec avec données invalides
  - Échec avec champs manquants
- ✅ Récupération d'utilisateurs (GET)
  - Succès par ID
  - Échec utilisateur inexistant
- ✅ Liste des utilisateurs (GET)
  - Liste avec utilisateurs
  - Liste vide
- ✅ Mise à jour d'utilisateurs (PUT)
  - Succès avec nouvelles données
  - Succès avec même email
  - Échec utilisateur inexistant
  - Échec email déjà utilisé par autre utilisateur
- ✅ Création d'amenities (POST)
  - Succès avec données valides
  - Échec avec données invalides
  - Échec avec champs manquants
- ✅ Récupération d'amenities (GET)
  - Succès par ID
  - Échec amenity inexistante
- ✅ Liste des amenities (GET)
  - Liste avec amenities
  - Liste vide
- ✅ Mise à jour d'amenities (PUT)
  - Succès avec nouvelles données
  - Échec amenity inexistante
  - Échec avec données invalides
- ✅ Gestion complète des codes d'erreur (400, 404, 201, 200)
- ✅ Validation stricte des données d'entrée

### **Tests de Services (Facade)**
- ✅ Gestion des utilisateurs
  - Création d'utilisateurs
  - Récupération par ID et email
  - Mise à jour avec validation
  - Liste complète des utilisateurs
- ✅ Logique métier
  - Validation d'unicité des emails
  - Gestion des cas d'erreur
  - Intégration avec les repositories
- ✅ Tests de couverture complète
  - Tous les cas de succès
  - Tous les cas d'échec
  - Cas limites et edge cases
- ✅ Gestion des amenities
  - Création d'amenities
  - Récupération par ID
  - Mise à jour avec validation
  - Liste complète des amenities
- ✅ Méthodes placeholder testées (get_place)

## 🆕 Nouveaux Tests Ajoutés

### **Tests API Supplémentaires**
- `test_update_user_same_email()` - Validation que la mise à jour avec le même email fonctionne
- `test_get_all_users_empty_list()` - Test de la liste vide d'utilisateurs
- `test_create_user_missing_fields()` - Validation des champs requis

### **Tests Amenities (NOUVEAUX)**
- `test_create_amenity_success()` - Création d'amenity avec succès
- `test_create_amenity_invalid_data()` - Création avec données invalides
- `test_get_amenity_success()` - Récupération par ID
- `test_get_all_amenities()` - Liste des amenities
- `test_update_amenity_success()` - Mise à jour avec succès
- `test_update_amenity_invalid_data()` - Mise à jour avec données invalides

### **Tests Services Supplémentaires**  
- `test_get_place()` - Test de récupération de lieu (méthode développée)
- `test_update_user_with_same_email()` - Test de mise à jour avec email identique

### **Tests Amenities Facade (NOUVEAUX)**
- `test_create_amenity()` - Création via facade
- `test_get_amenity()` - Récupération via facade
- `test_get_all_amenities()` - Liste via facade
- `test_update_amenity_success()` - Mise à jour via facade

## 🎯 Couverture de Tests Détaillée

### **Facade (Services) - 100% Couvert**
| Méthode | Tests | Scénarios Testés |
|---------|-------|------------------|
| `create_user()` | ✅ | Création normale |
| `get_user()` | ✅ | Succès + inexistant |
| `get_all_users()` | ✅ | Liste avec utilisateurs |
| `get_user_by_email()` | ✅ | Succès + inexistant |
| `update_user()` | ✅ | Succès + inexistant + email dupliqué + même email |
| `get_place()` | ✅ | ID inexistant |
| `create_amenity()` | ✅ | Création normale |
| `get_amenity()` | ✅ | Succès + inexistant |
| `get_all_amenities()` | ✅ | Liste avec amenities |
| `update_amenity()` | ✅ | Succès + inexistant + données invalides |

### **Endpoints API - 100% Couvert**
| Endpoint | Méthode | Tests | Scénarios Testés |
|----------|---------|-------|------------------|
| `/api/v1/users/` | POST | ✅ | Succès + email dupliqué + données invalides + champs manquants |
| `/api/v1/users/` | GET | ✅ | Liste avec utilisateurs + liste vide |
| `/api/v1/users/<id>` | GET | ✅ | Succès + inexistant |
| `/api/v1/users/<id>` | PUT | ✅ | Succès + inexistant + email dupliqué + même email |
| `/api/v1/amenities/` | POST | ✅ | Succès + données invalides + champs manquants |
| `/api/v1/amenities/` | GET | ✅ | Liste avec amenities + liste vide |
| `/api/v1/amenities/<id>` | GET | ✅ | Succès + inexistant |
| `/api/v1/amenities/<id>` | PUT | ✅ | Succès + inexistant + données invalides |

## 🚀 Prochaines Étapes

### **Tests à Développer**
1. **Tests de Persistence** - Repository et base de données
2. **Tests d'Intégration** - Flux complets end-to-end
3. **Tests de Performance** - Charge et stress
4. **Tests de Sécurité** - Validation et authentification

### **Améliorations Possibles**
- Tests de concurrence pour les emails
- Tests de validation avancée
- Tests de rollback et transactions
- Mocking avancé pour l'isolation
